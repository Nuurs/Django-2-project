from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permission import IsTeacher, IsAdmin

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]

    def get_queryset(self):
        if self.request.user.role == 'Teacher':
            # Teachers can only view attendance for their courses
            return Attendance.objects.filter(course__instructor=self.request.user)
        return Attendance.objects.all()  # Admins have full access
