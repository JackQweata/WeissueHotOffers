import telebot
from decouple import config
from ast import literal_eval
import re
from modules.channel_object import ChannelObject
from src.OZON.parser_management_ozon import ParserManagementOzon
from src.WB.parser_management_wb import ParserManagementWB
from src.bots.module.create_channel import NewCreateChannel
from src.bots.module.keyboard import channel_management_keyboard, back_keyboard, create_channel


def admin_commands_polling():
    bot = telebot.TeleBot(config("TOKEN_BOT_DEVELOPER"))
    admin_id = literal_eval(config("CHAT_ADMIN_ID"))
    new_create_channel = NewCreateChannel()

    @bot.message_handler(commands=['start'])
    def start_admin_bot(message):

        if message.chat.id not in admin_id:
            return bot.send_message(message.chat.id, 'Нет прав')
        markup = channel_management_keyboard()
        bot.send_message(message.chat.id, 'Привет', reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def commands_admin(message):
        channels = ChannelObject.channels_dict

        if message.chat.id not in admin_id:
            return bot.send_message(message.chat.id, 'Нет прав')

        for channel in channels.values():

            if message.text == f'{channel["class"].name} - Вкл':
                type_parser = channel['type']
                if not type_parser or type_parser == 3:
                    channel['thread'].stop_parser()
                    channel['thread'].join()
                if type_parser or type_parser == 3:
                    channel['mp'].stop_parser()
                    channel['mp'].join()

                channel["status"] = False
                markup = channel_management_keyboard()
                bot.send_message(message.chat.id, f'{channel["class"].name} остановлен', reply_markup=markup)
                break

            if message.text == f'{channel["class"].name} - Выкл':
                type_parser = channel['type']
                channels = channel['class']

                if not type_parser or type_parser == 3:
                    parser_management_wb = ParserManagementWB(channels)
                    parser_management_wb.start()
                    channel['thread'] = parser_management_wb

                if type_parser or type_parser == 3:
                    parser_management_oznon = ParserManagementOzon(channels)
                    parser_management_oznon.start()
                    channel['mp'] = parser_management_oznon

                channel["status"] = True
                markup = channel_management_keyboard()
                bot.send_message(message.chat.id, f'{channel["class"].name} запущен', reply_markup=markup)
                break

        if message.text == 'Создать канал':
            back_markup = back_keyboard(True)
            bot.send_message(message.chat.id, f'Заполните данные', reply_markup=back_markup)

        if message.text == 'Назад':
            markup = channel_management_keyboard()
            bot.send_message(message.chat.id, 'Главная', reply_markup=markup)

        if message.text == 'Проверить':
            is_carriage_information = True
            dict_new_create_channel = new_create_channel.dict_item()
            text = f'Проверьте информацию:\n\n' + \
                   '\n'.join([f"{key}: {value}" for key, value in dict_new_create_channel.items()])

            if 'не установлено' in [value for value in dict_new_create_channel.values()]:
                text += '\n\n Дополните информацию!!!'
                is_carriage_information = False

            inline_keyboard = create_channel(is_carriage_information)
            bot.send_message(message.chat.id, text=text, reply_markup=inline_keyboard)

        if re.search(r'\bназвание:', message.text.lower()):
            new_create_channel.name = message.text.split(":")[1].strip()
            bot.send_message(message.chat.id, 'Имя установлено, далее укажите цену (цена:)')

        if re.search(r'\bцена:', message.text.lower()):
            price = message.text.split(":")[1].strip()
            if not price.isdigit():
                return bot.send_message(message.chat.id, 'Укажите только цифры (цена:100)')

            new_create_channel.price = message.text.split(":")[1]
            bot.send_message(message.chat.id, 'Цена установлено, далее укажите ссылку/и на парсинг (ссылка:)')

        if re.search(r'\bссылка:', message.text.lower()):
            url = re.search(r'(https?://\S+)', message.text)
            if not url and url.split(':')[-1] != ('1' or '0'):
                return bot.send_message(message.chat.id, 'Укажите ссылку:тип')

            url = url.group(1)
            url_correct = url[:-2]

            if new_create_channel.url:
                return bot.send_message(message.chat.id, f'Ссылка добавлена, всего {len(new_create_channel.url)+1}')

            new_create_channel.url = {'url': url_correct, 'type': url[-1]}
            bot.send_message(message.chat.id, 'Ссылка установлено, далее укажите описание (описание:)')

        if re.search(r'\bописание:', message.text.lower()):
            new_create_channel.description = message.text.split(":")[1]
            print(message.text.split(":"))
            bot.send_message(message.chat.id, 'Описание установлено, далее укажите ID канала (ид:)')

        if re.search(r'\bид:', message.text.lower()):
            id_channel = message.text.split(":")[1].strip()
            if not id_channel.isdigit():
                return bot.send_message(message.chat.id, 'Укажите только цифры (ид:100000000)')

            new_create_channel.channel_id = id_channel
            bot.send_message(message.chat.id, 'ID канала установлено')

    @bot.callback_query_handler(func=lambda callback: True)
    def callback_command(callback):

        if callback.data == "not_create_channel":
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            return

        elif callback.data == "create_channel":
            bot.edit_message_text(
                text=f'Канал добавлен в бд\nДобавьте бота в канал и перезапустите скрипт',
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=None
            )
            new_create_channel.create_new_channel()

    bot.polling(none_stop=True)
