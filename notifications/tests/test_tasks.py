from notifications.tasks import send_grade_update_notification
from students.models import Student
from django.contrib.auth.models import User
from unittest.mock import patch

@patch("notifications.tasks.send_email")
def test_send_grade_notification(mock_send_email):
    student_user = User.objects.create_user(username="student", password="password")
    student = Student.objects.create(user=student_user, name="Test Student", email="test@student.com")
    
    send_grade_update_notification(student.id, "Math", "A")
    mock_send_email.assert_called_once_with(
        "Grade Update",
        "Your grade for Math is now A.",
        "from@example.com",
        ["test@student.com"],
    )
