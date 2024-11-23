from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema view configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Student Management System API",
        default_version='v1',
        description="API documentation for the Student Management System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@studentsystem.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),          # URL for users app
    path('api/students/', include('students.urls')),  # URL for students app
    path('api/courses/', include('courses.urls')),    # URL for courses app
    path('api/grades/', include('grades.urls')),      # URL for grades app
    path('api/attendance/', include('attendance.urls')),  # URL for attendance app

    # Swagger Documentation URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
]
