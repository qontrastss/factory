from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='registration'),
    path('auth/', views.UserAuthView.as_view(), name='authentication'),
]