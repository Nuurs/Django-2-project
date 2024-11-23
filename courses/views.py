from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from users.permission import IsTeacher, IsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing, creating, retrieving, updating, and deleting courses.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['instructor']
    search_fields = ['name', 'description']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        """
        Custom action to enroll a student in a course.
        """
        course = self.get_object()
        Enrollment.objects.create(course=course, student=request.user)
        return Response({'message': 'Enrolled successfully!'})


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing enrollments.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]

    def perform_create(self, serializer):
        """
        Ensure only teachers can enroll students in their courses.
        """
        if self.request.user.role == 'Teacher':
            serializer.save(instructor=self.request.user)
        else:
            raise PermissionDenied("Only teachers can create enrollments.")
