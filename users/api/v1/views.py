# views.py
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserAuthSerializer, UserRegistrationResponseSerializer
from ...authentication import token_expire_handler, expires_in

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserRegisterView(APIView):
    @swagger_auto_schema(
        operation_description="API for registration",
        request_body=UserRegistrationSerializer,
        responses={
            201: UserRegistrationResponseSerializer,
            400: 'Bad Request',
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            new_user = serializer.save()
            return Response(UserRegistrationResponseSerializer(new_user).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuthView(APIView):
    @swagger_auto_schema(
        operation_description="API for authorization",
        request_body=UserAuthSerializer,
        responses={
            200: "User registered successfully",
            403: 'Invalid Credentials',
        }
    )
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if not user:
            return Response('Invalid Credentials', status=status.HTTP_403_FORBIDDEN)
        token, created = Token.objects.get_or_create(user=user)

        is_expired, token = token_expire_handler(token)

        return Response({
            'expires_in': expires_in(token),
            'token': token.key
        }, status=status.HTTP_200_OK)