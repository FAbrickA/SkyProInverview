from rest_framework import fields, serializers

from . import models


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resume
        fields = (
            "status",
            "grade",
            "speciality",
            "salary",
            "education",
            "experience",
            "portfolio",
            "title",
            "phone",
            "email",
        )