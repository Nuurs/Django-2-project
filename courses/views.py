from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from users.permission import IsTeacher, IsAdmin

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]

    def perform_create(self, serializer):
        # Ensure only teachers can enroll students in their courses
        if self.request.user.role == 'Teacher':
            serializer.save(instructor=self.request.user)
