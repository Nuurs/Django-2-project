from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer
from users.permission import IsStudent, IsAdmin, IsTeacher
from rest_framework import generics, permissions
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from .decorators import track_api_usage 



class StudentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsStudent | IsAdmin]

    def get_queryset(self):
        # Students can only view their own records
        if self.request.user.role == 'Student':
            return Student.objects.filter(user=self.request.user)
        return Student.objects.all()

@method_decorator(cache_page(60 * 15), name='dispatch')
class StudentListView(generics.ListCreateAPIView):
    """
    Handles listing all students (teachers and admins only)
    and creating a new student (admins only).
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            # Only admins can create new students
            return [permissions.IsAuthenticated(), IsAdmin()]
        else:
            # Teachers and admins can view the student list
            return [permissions.IsAuthenticated(), IsAdmin() | IsTeacher()]

    def get_queryset(self):
        """
        Customize queryset:
        - Teachers can view students in their own courses.
        - Admins can view all students.
        """
        user = self.request.user
        if user.role == 'Teacher':
            # Return students enrolled in courses taught by this teacher
            return Student.objects.filter(
                enrollment__course__instructor=user
            ).distinct()
        return super().get_queryset()  # Admins see all students
    

@swagger_auto_schema(operation_description="Get all students")
@api_view(['GET'])
@track_api_usage 
def get_students(request):
    students = Student.objects.all()  # Get all students from the database
    student_data = [
        {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            # Add any other fields you need here
        }
        for student in students
    ]
    return Response(student_data)
