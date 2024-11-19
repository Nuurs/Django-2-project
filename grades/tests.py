from django.urls import reverse
from rest_framework.test import APITestCase
from grades.models import Grade
from courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

class GradeTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="pass", role="Teacher")
        self.student = User.objects.create_user(username="student", password="pass", role="Student")
        self.course = Course.objects.create(title="Math 101", description="Introductory math", teacher=self.teacher)
        self.grade_url = reverse("assign-grade", args=[self.student.id, self.course.id])  # Adjust args dynamically

    def test_grade_assignment(self):
        self.client.login(username="teacher", password="pass")
        response = self.client.post(self.grade_url, {"grade": "A"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Grade.objects.filter(student=self.student, course=self.course).count(), 1)

    def test_student_cannot_assign_grade(self):
        self.client.login(username="student", password="pass")
        response = self.client.post(self.grade_url, {"grade": "A"})
        self.assertEqual(response.status_code, 403)
