from rest_framework import viewsets, permissions, generics, status
from forms.models import Form, Submission
from forms.serializers import FormSerializer, FormDetailSerializer, SubmissionSerializer
from rest_framework.response import Response

class FormViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return FormDetailSerializer
        
        return FormSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.AllowAny()]
        
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.action == "retrieve":
            return Form.objects.all()

        return Form.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class SubmitResponseView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        form_id = request.data.get("form")
        
        try:
            form = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return Response({"error": "Form Does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if not form.is_accepting_responses:
            return Response({"error": "Form is closed and currently not accepting any responses."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)
