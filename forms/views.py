from rest_framework import viewsets, permissions
from forms.models import Form
from forms.serializers import FormSerializer

class FormViewSet(viewsets.ModelViewSet):
    serializer_class = FormSerializer

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