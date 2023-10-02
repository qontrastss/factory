import os

import telebot

token = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)