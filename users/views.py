from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

def login_view(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        # Process login form
        pass
 
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    """
    Handle user signup.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({"message": "User created successfully",
                         "user_id": user.id,
                         "refresh": str(refresh),
                         "access": str(refresh.access_token)
                }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)