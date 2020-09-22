from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated



class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request,):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=username, email=email, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    #authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"email": request.user.email})
