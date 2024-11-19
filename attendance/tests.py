from django.urls import reverse
from rest_framework.test import APITestCase
from attendance.models import Attendance
from courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

class AttendanceTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="pass", role="Teacher")
        self.student = User.objects.create_user(username="student", password="pass", role="Student")
        self.course = Course.objects.create(title="Math 101", description="Introductory math", teacher=self.teacher)
        self.attendance_url = reverse("mark-attendance", args=[self.student.id, self.course.id])  # Adjust args dynamically

    def test_mark_attendance(self):
        self.client.login(username="teacher", password="pass")
        response = self.client.post(self.attendance_url, {"status": "Present"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Attendance.objects.filter(student=self.student, course=self.course).count(), 1)

    def test_student_cannot_mark_attendance(self):
        self.client.login(username="student", password="pass")
        response = self.client.post(self.attendance_url, {"status": "Present"})
        self.assertEqual(response.status_code, 403)
