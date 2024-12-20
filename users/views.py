from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, ProfileSerializer
from .models import Profile
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.shortcuts import render
from .models import ApiRequest
from django.db.models import Count 

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(APIView):
    """Handle user registration."""

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.profile.role == "Admin":
            profiles = Profile.objects.all()
        elif user.profile.role == "Teacher":
            profiles = Profile.objects.filter(role="Student")
        else:  # Default to viewing the student's own profile
            profiles = Profile.objects.filter(user=user)

        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def active_users_view(request):
    # Get the most active users
    active_users = ApiRequest.objects.values('user').annotate(request_count=Count('id')).order_by('-request_count')
    
    # Pass the result to a template or return as JSON
    return render(request, 'analytics/active_users.html', {'active_users': active_users})
