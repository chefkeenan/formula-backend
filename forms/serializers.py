from rest_framework import serializers
from forms.models import Form

class FormSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Form
        fields = ("id", "title", "description", "creator", "created_at", "updated_at")