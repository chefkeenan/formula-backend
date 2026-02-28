from django.db import models
from django.contrib.auth.models import User
import uuid

class Form(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forms")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ("text", "Short Answer"),
        ("textarea", "Paragraph"),
        ("radio", "Multiple Choice"),
        ("checkbox", "Checkboxes"),
        ("dropdown", "Dropdown"),
    ]

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    type = models.CharField(max_length=20, choices=QUESTION_TYPES, default="text")
    question_text = models.CharField(max_length=500, blank=True)
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.form.title} - {self.question_text}"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    option_text = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.option_text