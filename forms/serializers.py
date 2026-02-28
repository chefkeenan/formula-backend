from rest_framework import serializers
from forms.models import Form, Option, Question

class FormSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Form
        fields = ("id", "title", "description", "creator", "created_at", "updated_at")

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

    class Meta:
        model = Form
        fields = ["id", "title", "description", "creator", "created_at", "updated_at", "questions"]

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        questions_data = self.initial_data.get("questions")
        
        if questions_data is not None:
            existing_question_ids = [q.id for q in instance.questions.all()]
            incoming_question_ids = []

            for index, q_data in enumerate(questions_data):
                q_id = q_data.get("id")
                
                if isinstance(q_id, int) or (isinstance(q_id, str) and q_id.isdigit()):
                    q_instance = Question.objects.get(id=int(q_id), form=instance)
                    
                    q_instance.question_text = q_data.get("question_text", q_instance.question_text)
                    q_instance.type = q_data.get("type", q_instance.type)
                    q_instance.required = q_data.get("required", q_instance.required)
                    q_instance.order = index
                    q_instance.save()
                    
                    incoming_question_ids.append(q_instance.id)
                    self._update_options(q_instance, q_data.get("options", []))
                    
                else:
                    new_q = Question.objects.create(
                        form=instance,
                        type=q_data.get("type", "text"),
                        question_text=q_data.get("question_text", ""),
                        required=q_data.get("required", False),
                        order=index
                    )
                    incoming_question_ids.append(new_q.id)
                    self._update_options(new_q, q_data.get("options", []))

            questions_to_delete = set(existing_question_ids) - set(incoming_question_ids)
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