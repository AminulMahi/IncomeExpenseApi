from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import jwt
from .models import User
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer

from drf_yasg.utils import swagger_auto_schema  #manual param
from drf_yasg import openapi  #manual param
# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def get(self, request):
        user_obj = User.objects.all()
        serializer = self.serializer_class(user_obj, many=True)
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_202_ACCEPTED)
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            user_errors = serializer.errors
            return Response(user_errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        user_data = serializer.data     # getting the user request

        user = User.objects.get(email = user_data['email'])  #getting the user email from DB

        token = RefreshToken.for_user(user).access_token      # generate token for user

        current_site = get_current_site(request).domain    #getting current site domain 127.0.0.1:8000

        relative_link = reverse('email_verify')   #getting reverse url

        fullUrl = 'http://'+current_site+relative_link+'?token='+str(token)  #combine the url
        
        email_sub = "Welcome to our website"
        email_body = '!Hi'+ user.username + 'use link below to verify you email \n' + fullUrl
        sender_mail = settings.EMAIL_HOST   
        send_mail(email_sub, email_body, sender_mail, [user.email]) #sending email to user

        # send_mail(email_subject, body_link, sender_email, [reciver_email])


        return Response(user_data, status=status.HTTP_201_CREATED) 
    

class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    token_param = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Despription', type=openapi.TYPE_STRING)
    # manual parameter
    @swagger_auto_schema(manual_parameters=[token_param])
    def get(self, request):
        token = request.GET.get('token')  # getting token from user request

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(payload)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True  # Corrected the assignment
                user.save()
                return Response({'success': 'email successfully activated'}, status=status.HTTP_200_OK)
            else:
                return Response({'info': 'email already verified'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'errors': 'activation expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'errors': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'errors': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
            


class LoginApiview(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)