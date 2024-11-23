from django.urls import path
from .views import StudentListView, StudentDetailView
from . import views

urlpatterns = [
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('students/', views.get_students, name='get_students'),
]
