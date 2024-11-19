from django.db import models
from users.models import User
from students.models import Student

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
