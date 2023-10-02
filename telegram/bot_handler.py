from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from telegram.bot import bot
from telegram.models import TelegramUser, TelegramUserConnectTry


# def check_connection_tries(chat_id) -> bool:
#


def handle_message(message, chat_id) -> None:

    connection_try = TelegramUserConnectTry.objects.filter(chat_id=chat_id).order_by('created_at').last()

    if connection_try and connection_try.is_successful is None:  # If user inputted login and writes password
        user = authenticate(username=connection_try.user, password=message)

        if user:  # if authentications is succeeded
            connection_try.is_successful = True
            connection_try.save()
            telegram_users = TelegramUser.objects.filter(user=user)
            if telegram_users:
                current_user = telegram_users.filter(chat_id=chat_id).first()
                if current_user:
                    current_user.is_active = True
                    for iterate_user in telegram_users.exclude(id=current_user.id):
                        iterate_user.is_active = False
                        iterate_user.save()
                else:
                    for iterate_user in telegram_users:
                        iterate_user.is_active = False
                        iterate_user.save()
                    TelegramUser.objects.create(user=user, chat_id=chat_id)
            else:
                TelegramUser.objects.create(user=user, chat_id=chat_id)

            bot.send_message(chat_id, "Поздравляю вы успешно подтвердили данные!")
            bot.send_message(chat_id, "Если хотите привязать к другому аккаунту, просто введите логин:")
            print("Поздравляю вы успешно подтвердили данные!")
            print("Если хотите привязать к другому аккаунту, просто введите логин:")
            return
        else:
            connection_try.is_successful = False
            connection_try.save()
            bot.send_message(chat_id, "Вы ввели неправильные данные!")
            bot.send_message(chat_id, "Введите логин:")
            print("Вы ввели неправильные данные!")
            print("Введите логин:")
            return
    else:  # if there is user tries to connect to account
        user = User.objects.filter(username=message).first()
        if user:
            TelegramUserConnectTry.objects.create(chat_id=chat_id, user=user)
            bot.send_message(chat_id, "Введите пароль:")
            print("Введите пароль:")
            return
        else:
            bot.send_message(chat_id, "Пользователь с таким логином не найден, введите еще раз:")
            print("Пользователь с таким логином не найден, введите еще раз:")
            return
