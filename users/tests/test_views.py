from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class UserViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="adminpass", role="Admin")
        self.student = User.objects.create_user(username="student", password="studentpass", role="Student")
        self.client.login(username="admin", password="adminpass")

    def test_register_user(self):
        url = "/api/auth/register/"
        data = {"username": "newuser", "password": "password123", "role": "Student"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_access_restriction(self):
        self.client.login(username="student", password="studentpass")
        url = "/api/students/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
