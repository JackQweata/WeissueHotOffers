import telebot
from ast import literal_eval
from decouple import config


def send_message(type_mess, message):
    bot = telebot.TeleBot(config("TOKEN_BOT_DEVELOPER"))
    admin_id = literal_eval(config("CHAT_ADMIN_ID"))

    for a_id in admin_id:
        bot.send_message(chat_id=a_id, text=f"[{type_mess}]   {message}")
