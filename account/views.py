from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully", "status": True, "data": {}}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = user.get_tokens
            return Response({"message": "User logged in successfully", "data": tokens, "status": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        data = serializer.data
        return Response({"message": "User details retrieved successfully", "data": data, "status": True}, status=status.HTTP_200_OK)
    
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({"message": "User details updated successfully", "data": data, "status": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AllUserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.filter(is_active = True)
        serializer = UserSerializer(users, many = True)
        return Response({"message": "User details retrieved successfully", "data": serializer.data, "status": True}, status=status.HTTP_200_OK)