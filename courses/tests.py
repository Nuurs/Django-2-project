from django.urls import reverse
from rest_framework.test import APITestCase
from courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

class CourseTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.course_url = reverse("course-list")  # Adjust name as per your routes
        cls.enrollment_url = reverse("enroll-course", args=[1])  # Adjust args dynamically

    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="pass", role="Teacher")
        self.student = User.objects.create_user(username="student", password="pass", role="Student")

        self.course = Course.objects.create(
            title="Math 101", description="Introductory math", teacher=self.teacher
        )

    def test_course_creation(self):
        self.client.login(username="teacher", password="pass")
        response = self.client.post(self.course_url, {
            "title": "Science 101",
            "description": "Introductory science",
            "teacher": self.teacher.id,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Course.objects.count(), 2)

    def test_enrollment(self):
        self.client.login(username="student", password="pass")
        response = self.client.post(self.enrollment_url)
        self.assertEqual(response.status_code, 200)
