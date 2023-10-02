from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_telegram_message),
    path('send/', views.SendMessageView.as_view()),
    path('messages/', views.GetMessagesView.as_view()),
]