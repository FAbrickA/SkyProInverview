from django.db import models
from django.utils.translation import gettext_lazy as _


class Resume(models.Model):
    class ResumeStatus(models.IntegerChoices):
        NOT_READ = 0, _("Not read")
        READ = 1, _("Read")
        APPLIED = 2, _("Applied")
        DENIED = 3, _("Denied")
        ARCHIVED = 4, _("Archived")

    status = models.IntegerField(choices=ResumeStatus.choices, default=ResumeStatus.NOT_READ)
    grade = models.IntegerField(null=True, default=None)
    speciality = models.CharField(max_length=255)
    salary = models.IntegerField(null=True, default=None)
    education = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    portfolio = models.CharField(max_length=1000, null=True, default=None)
    title = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
