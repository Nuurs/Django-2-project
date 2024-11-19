from django.core.cache import cache
from rest_framework.test import APITestCase
from students.models import Student
from django.contrib.auth.models import User

class CachingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass", role="Admin")
        self.client.login(username="testuser", password="testpass")
        self.student = Student.objects.create(user=self.user, name="Test Student", email="test@student.com")

    def test_student_list_cache(self):
        url = "/api/students/"
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)

        # Add a new student and check the cache still serves old data
        Student.objects.create(user=self.user, name="Another Student", email="another@student.com")
        response2 = self.client.get(url)
        self.assertEqual(len(response2.data), 1)  # Cache returns old data

        # Clear the cache
        cache.clear()
        response3 = self.client.get(url)
        self.assertEqual(len(response3.data), 2)  # Now shows updated data
