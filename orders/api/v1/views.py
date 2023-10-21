# views.py
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.parsers import FileUploadParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OrderSerializer, OrderDetailSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ...models import Order

header_param = openapi.Parameter('Bearer', openapi.IN_HEADER, description="Bearer header param is required", type=openapi.IN_HEADER)


class OrderAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = OrderSerializer
    parser_class = (FileUploadParser,)

    @swagger_auto_schema(
        operation_description="API for making order. Request body is multipart/form-data. [POST /api/v1/order/]",
        request_body=OrderSerializer,
        responses={
            201: OrderSerializer,
            403: 'Invalid Credentials',
        }
    )
    def post(self, request):
        from orders.tasks import process_order
        process_order.delay(order_code='J532IA')
        serializer = self.serializer_class(data=request.data, context={'request': request,
                                                                       'files': request.FILES})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.serializer_class(instance).data, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = OrderDetailSerializer

    @swagger_auto_schema(
        operation_description="API for retrieving information about order. Token is not required. [GET /api/v1/order/{code}/]",
        manual_parameters=[header_param],
        responses={
            201: OrderDetailSerializer,
            403: 'Invalid Credentials',
        }
    )
    def get(self, request, *args, **kwargs):
        code = self.kwargs.get("code")
        if request.user.is_anonymous:
            instance = Order.objects.filter(code=code, user__isnull=True).first()
        else:
            instance = Order.objects.filter(Q(user=request.user) | Q(user__isnull=True), code=code).first()
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)