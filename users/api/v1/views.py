from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, UserUpdateSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


header_param = openapi.Parameter('Bearer', openapi.IN_HEADER, description="Bearer header param is required", type=openapi.IN_HEADER)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    parser_class = (FileUploadParser,)

    @swagger_auto_schema(
        operation_description="API for registration. Request body is multipart/form-data. [GET /api/v1/user/register/]",
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            403: 'Invalid Credentials',
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()
        return Response(self.serializer_class(new_user).data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    parser_class = (FileUploadParser,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'PUT':
            return UserUpdateSerializer
        return UserSerializer

    @swagger_auto_schema(
        operation_description="API for retrieving information about user. [GET /api/v1/user/profile/]",
        manual_parameters=[header_param],
        responses={
            200: UserSerializer,
            401: '{"detail": "Given token not valid for any token type", "code": "token_not_valid", "messages": [{'
                 '"token_class": "AccessToken", "token_type": "access", "message": "Token is invalid or expired"}]}',
        }
    )
    def get(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="API for retrieving information about user. Request body is multipart/form-data. [PUT "
                              "/api/v1/user/profile/]",
        manual_parameters=[header_param],
        request_body=UserUpdateSerializer,
        responses={
            200: UserUpdateSerializer,
            401: '{"detail": "Given token not valid for any token type", "code": "token_not_valid", "messages": [{'
                 '"token_class": "AccessToken", "token_type": "access", "message": "Token is invalid or expired"}]}',
        }
    )
    def put(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
