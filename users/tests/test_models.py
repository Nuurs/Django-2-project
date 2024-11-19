import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(username="testuser", password="password123", role="Student")
    assert user.username == "testuser"
    assert user.check_password("password123")
    assert user.role == "Student"
