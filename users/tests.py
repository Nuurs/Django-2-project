from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import Profile

User = get_user_model()

class UserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Define URLs for authentication and registration
        cls.registration_url = reverse("user-register")  # Replace with your actual route name
        cls.login_url = reverse("token_obtain_pair")  # Assuming JWT authentication
        cls.profile_url = reverse("profile-detail")  # Adjust as needed

    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(
            username="admin", password="adminpass", email="admin@example.com"
        )
        self.teacher_user = User.objects.create_user(
            username="teacher", password="teacherpass", email="teacher@example.com"
        )
        self.student_user = User.objects.create_user(
            username="student", password="studentpass", email="student@example.com"
        )

        # Ensure profiles are created without duplication
        Profile.objects.get_or_create(user=self.admin_user, role="Admin")
        Profile.objects.get_or_create(user=self.teacher_user, role="Teacher")
        Profile.objects.get_or_create(user=self.student_user, role="Student")

    def get_token(self, username, password):
        """Helper function to get an authentication token."""
        response = self.client.post(self.login_url, {"username": username, "password": password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["access"]

    def test_user_registration(self):
        response = self.client.post(self.registration_url, {"username": "test", "password": "password123"})
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        """Ensure a user can log in and receive a valid token."""
        response = self.client.post(self.login_url, {"username": "admin", "password": "adminpass"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_invalid_login(self):
        """Ensure login fails with invalid credentials."""
        response = self.client.post(self.login_url, {"username": "admin", "password": "wrongpassword"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_role_based_access_admin(self):
        """Ensure an admin has full access to all profiles."""
        token = self.get_token("admin", "adminpass")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.profile_url)  # Adjust endpoint for admin view
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 1)  # Admin can see multiple profiles

    def test_role_based_access_teacher(self):
        """Ensure a teacher can view and update student profiles but not admin profiles."""
        token = self.get_token("teacher", "teacherpass")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.profile_url)  # Adjust endpoint for teacher view
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("Admin", [profile["role"] for profile in response.data])  # Replace with correct data structure

    def test_role_based_access_student(self):
        """Ensure a student can only view and update their profile."""
        token = self.get_token("student", "studentpass")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.profile_url)  # Adjust endpoint for student profile
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "student")

    def test_update_profile(self):
        """Ensure a user can update their profile information."""
        token = self.get_token("student", "studentpass")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.patch(self.profile_url, {"bio": "Updated bio"})  # Adjust based on your model
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student_user.refresh_from_db()
        self.assertEqual(self.student_user.profile.bio, "Updated bio")
