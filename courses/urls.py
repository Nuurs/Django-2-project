from django.urls import path
from .views import CourseViewSet, EnrollmentViewSet

urlpatterns = [
    path('', CourseViewSet.as_view(), name='course-list'),
    path('enroll/', EnrollmentViewSet.as_view(), name='enroll-student'),
]
