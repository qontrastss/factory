from django.urls import path
from . import views
from .views import UserRetrieveUpdateAPIView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', views.RegistrationAPIView.as_view(), name='registration'),
    path('profile/', UserRetrieveUpdateAPIView.as_view()),
]