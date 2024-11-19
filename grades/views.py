from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Grade
from .serializers import GradeSerializer
from users.permission import IsTeacher, IsAdmin

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]

    def get_queryset(self):
        if self.request.user.role == 'Teacher':
            # Teachers can only view grades for their courses
            return Grade.objects.filter(course__instructor=self.request.user)
        return Grade.objects.all()  # Admins have full access
