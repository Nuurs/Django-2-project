from django.urls import path
from .views import GradeViewSet

urlpatterns = [
    path('', GradeViewSet.as_view(), name='grade-list'),
]
