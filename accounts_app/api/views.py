from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import  AllowAny

from .serializers import RegisterSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, ActivateAccountSerializer

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts_app.models import CustomUser

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

import django_rq
from accounts_app.tasks import send_activation_email

# Create your views here.
class RegisterView(CreateAPIView):
    """
    View for user registration.

    Provides an endpoint for creating new user accounts.
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    


class ActivateAccountView(APIView):
    """
    View to activate user account via activation link.
    """
    serializer_class = ActivateAccountSerializer
    
    def post(self, request, *args, **kwargs):
       serializer = self.serializer_class(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response({"detail": "The account has been successfully activated."}, status=status.HTTP_200_OK)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
 
        
class LoginView(APIView):
    """
    View to login the user and receive refresh and access tokens for authentication.
    """
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
                # generate token
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
        else:
            # resend activation link if not user.is_active
            try: 
                user = CustomUser.objects.get(email=email)
                if user and not user.is_active:
                    django_rq.enqueue(send_activation_email, user)
            except:
                pass
      
            return Response({"detail": "Account could not be verified. Please check your credentials or activate your account if necessary."}, status=status.HTTP_401_UNAUTHORIZED)
         

class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "An email has been sent if an account with this email exists."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "The password has been successfully reset."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)