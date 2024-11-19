from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet)
router.register('enrollments', EnrollmentViewSet)

urlpatterns = router.urls
    