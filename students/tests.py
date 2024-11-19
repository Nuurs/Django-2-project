from django.test import TestCase
from .models import Student

class StudentModelTest(TestCase):
    def test_create_student(self):
        student = Student.objects.create(name="John Doe", dob="2000-01-01")
        self.assertEqual(student.name, "John Doe")
