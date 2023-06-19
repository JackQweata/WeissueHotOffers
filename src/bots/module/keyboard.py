from telebot import types
from modules.channel_object import ChannelObject


def channel_management_keyboard():
    channels = ChannelObject.channels_dict
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for channel in channels.values():
        status_channel = 'Вкл' if channel['status'] else 'Выкл'
        markup.add(types.KeyboardButton(f'{channel["class"].name} - {status_channel}'))

    markup.add(types.KeyboardButton('Создать канал'))
    return markup


def back_keyboard(additional_keyboard=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if additional_keyboard:
        markup.add(types.KeyboardButton('Проверить'))
    markup.add(types.KeyboardButton(f'Назад'))
    return markup


def create_channel(is_carriage_information):
    keyboard = types.InlineKeyboardMarkup()
    if is_carriage_information:
        keyboard.add(types.InlineKeyboardButton("Да", callback_data=f"create_channel"))

    keyboard.add(types.InlineKeyboardButton("Нет", callback_data="not_create_channel"))
    return keyboard
