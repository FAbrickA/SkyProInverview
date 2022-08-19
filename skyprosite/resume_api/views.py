from django.http import JsonResponse, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view

from resume_api.models import Resume
from resume_api.serializers import ResumeSerializer


@api_view(["GET", "PATCH"])
def resume(request):
    if request.method == "GET":
        resume = Resume.objects.first()
        return JsonResponse(
            ResumeSerializer(resume).data,
        )

    else:  # if request.method == "PATCH":
        user = request.user
        if user.is_anonymous:
            return HttpResponseForbidden("You need to log in to continue")
        if not user.is_superuser:
            return HttpResponseForbidden("Access denied. Only superuser can patch the data")
        resume = Resume.objects.first()
        data = request.data
        try:
            for key, value in data.items():
                getattr(resume, key)  # will raise AttributeError if key doesn't exist in resume
                setattr(resume, key, value)
        except AttributeError:
            return HttpResponseBadRequest("Invalid input data")
        resume.save()
        return HttpResponse()
