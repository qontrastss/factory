import os
from dotenv import load_dotenv

import telebot

load_dotenv()

token = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)