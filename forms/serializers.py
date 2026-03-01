from rest_framework import serializers
from forms.models import Form, Option, Question, Submission, Answer
from rest_framework.exceptions import ValidationError
from django.db import transaction

class FormSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")
    responses_count = serializers.SerializerMethodField()

    class Meta:
        model = Form
        fields = ("id", "title", "description", "creator", "created_at", "updated_at", "is_accepting_responses", "responses_count")

    def get_responses_count(self, obj):
        return obj.submissions.count()

class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ["id", "type", "question_text", "required", "options", "order"]

    def get_options(self, obj):
        return [opt.option_text for opt in obj.options.all().order_by('order')]

class FormDetailSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")
    questions = QuestionSerializer(many=True, read_only=True)
    has_submissions = serializers.SerializerMethodField()

    class Meta:
        model = Form
        fields = ["id", "title", "description", "creator", "created_at", "updated_at", "questions", "is_accepting_responses", "has_submissions"]

    def get_has_submissions(self, obj):
        return obj.submissions.exists()

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.is_accepting_responses = validated_data.get("is_accepting_responses", instance.is_accepting_responses)
        instance.save()

        questions_data = self.initial_data.get("questions")
        
        if questions_data is not None:
            has_submissions = instance.submissions.exists()

            existing_question_ids = {str(q.id) for q in instance.questions.all()}
            incoming_question_ids = []

            for index, q_data in enumerate(questions_data):
                q_id = str(q_data.get("id", ""))
                
                if q_id in existing_question_ids:
                    q_instance = Question.objects.get(id=q_id, form=instance)
                    
                    new_type = q_data.get("type", q_instance.type)
                    
                    if has_submissions and q_instance.type != new_type:
                        raise ValidationError({"questions": f"Can't change the question type '{q_instance.question_text}'. Form already has submissions."})
                    
                    q_instance.question_text = q_data.get("question_text", q_instance.question_text)
                    q_instance.type = new_type
                    q_instance.required = q_data.get("required", q_instance.required)
                    q_instance.order = index
                    q_instance.save()
                    
                    incoming_question_ids.append(str(q_instance.id))
                    self._update_options(q_instance, q_data.get("options", []))
                    
                else:
                    new_q = Question.objects.create(
                        form=instance,
                        type=q_data.get("type", "text"),
                        question_text=q_data.get("question_text", ""),
                        required=q_data.get("required", False),
                        order=index
                    )
                    incoming_question_ids.append(str(new_q.id))
                    self._update_options(new_q, q_data.get("options", []))

            questions_to_delete = existing_question_ids - set(incoming_question_ids)
            
            if questions_to_delete and has_submissions:
                raise ValidationError({"questions": "Can't make changes. Form already has submissions"})
                
            Question.objects.filter(id__in=questions_to_delete).delete()

        return instance

    def _update_options(self, question_instance, options_data):
        question_instance.options.all().delete()
        for opt_index, opt_text in enumerate(options_data):
            Option.objects.create(
                question=question_instance,
                option_text=opt_text,
                order=opt_index
            )

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["question", "answer_text"]

class SubmissionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Submission
        fields = ["id", "form", "submitted_at", "answers"]
        read_only_fields = ["id", "submitted_at"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers", [])
        submission = Submission.objects.create(**validated_data)
        
        for answer_data in answers_data:
            Answer.objects.create(submission=submission, **answer_data)
            
        return submission