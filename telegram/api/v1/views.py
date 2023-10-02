# views.py
import logging

from rest_framework import status, generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from telegram.api.v1.serializers import MessageSerializer, MessageBodySerializer
from telegram.bot import bot
from telegram.bot_handler import handle_message
from telegram.models import TelegramUserConnectTry, TelegramUser, Message


@api_view(["POST"])
@permission_classes((AllowAny,))
def get_telegram_message(request):
    try:
        chat_id = request.data["message"]["chat"]["id"]
        message = request.data["message"]["text"]
    except Exception as e:
        logging.error(f"Error at telegram bot logic!!! Error: {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if message == '/start':  # restarts bot and we should clean all data
        TelegramUserConnectTry.objects.filter(chat_id=chat_id).delete()
        TelegramUser.objects.filter(chat_id=chat_id).delete()
        bot.send_message(chat_id, "Введите логин:")
    else:
        handle_message(message=message, chat_id=chat_id)

    return Response(status=status.HTTP_200_OK)


class SendMessageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageBodySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data['text']

        telegram_user = TelegramUser.objects.filter(user=request.user).first()
        if not telegram_user:
            return Response({'detail': 'Telegram account is not connected, please connect it'}, status=status.HTTP_400_BAD_REQUEST)

        bot.send_message(telegram_user.chat_id, text)
        print(text)
        Message.objects.create(telegram=telegram_user, text=text)
        return Response(status=status.HTTP_201_CREATED)


class GetMessagesView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        telegram_user = TelegramUser.objects.filter(user=request.user).first()
        if not telegram_user:
            return Response({'detail': 'Telegram account is not connected, please connect it'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(telegram_user.message_set.all(), many=True).data, status=status.HTTP_201_CREATED)

