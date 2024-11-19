from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("register/", views.RegisterView.as_view(), name="user-register"),
    path("login/", views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("profile/", views.ProfileDetailView.as_view(), name="profile-detail"),
]
