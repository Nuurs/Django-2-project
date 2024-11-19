from django.urls import path
from .views import AttendanceViewSet

urlpatterns = [
    path('mark/', AttendanceViewSet.as_view(), name='mark-attendance'),
]
