from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Resume


class ResumeTests(APITestCase):
    def setUp(self):
        Resume(
            status=1,
            grade=2,
            speciality="Специальность",
            salary=123456,
            education="Образование",
            experience="Опыт работы",
            portfolio="Портфолио",
            title="Заголовок",
            phone="+79000000000",
            email="someemail@email.com"
        ).save()
        User.objects.create_superuser("admin", password="coolpassword123")
        User.objects.create_user("commonUser", password="strongpassword321")

    def test_get_resume(self):
        """ GET /resume """
        response = self.client.get("/resume")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "grade": 2,
                "status": 1,
                "speciality": "Специальность",
                "salary": 123456,
                "education": "Образование",
                "experience": "Опыт работы",
                "portfolio": "Портфолио",
                "title": "Заголовок",
                "phone": "+79000000000",
                "email": "someemail@email.com",
            }
        )

    def test_patch_resume_anonymous(self):
        """ PATCH /resume
            AnonymousUser """
        response = self.client.patch("/resume", data={"education": "Новое образование"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        resume = Resume.objects.first()
        self.assertNotEqual(resume.education, "Новое образование")

    def test_patch_resume_common_user(self):
        """ PATCH /resume
            Common User without staff or superuser status """
        self.client.force_login(User.objects.get(username="commonUser"))
        response = self.client.patch("/resume", data={"education": "Новое образование"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        resume = Resume.objects.first()
        self.assertNotEqual(resume.education, "Новое образование")

    def test_patch_resume_superuser(self):
        """ PATCH /resume
            Superuser """
        self.client.force_login(User.objects.get(username="admin"))
        response = self.client.patch("/resume", data={"education": "Новое образование"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resume = Resume.objects.first()
        self.assertEqual(resume.education, "Новое образование")

        response = self.client.patch("/resume", data={
            "salary": 333333,
            "educationnnn": "Образованннние",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resume.salary, 123456)
