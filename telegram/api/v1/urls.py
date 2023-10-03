from django.urls import path
from . import views


urlpatterns = [
    path('', views.GetTelegramMessageView.as_view()),
    path('send/', views.SendMessageView.as_view()),
    path('messages/', views.GetMessagesView.as_view()),
]