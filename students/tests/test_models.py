import pytest
from students.models import Student
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_student_creation():
    user = User.objects.create_user(username="teststudent", password="password123")
    student = Student.objects.create(user=user, name="Test Student", email="test@example.com")
    
    assert student.name == "Test Student"
    assert student.email == "test@example.com"
    assert student.user == user
