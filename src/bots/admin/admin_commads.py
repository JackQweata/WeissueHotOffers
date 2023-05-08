import telebot
from decouple import config
from telebot import types
from ast import literal_eval
from src.WB.module.parser_management import ParserManagementWB
from src.WB.run_parser import start_parse
from utils.run_threading import start_threading


def commands():
    bot = telebot.TeleBot(config("TOKEN_BOT_DEVELOPER"))
    admin_id = literal_eval(config("CHAT_ADMIN_ID"))
    management = ParserManagementWB()

    @bot.message_handler(commands=['start'])
    def start_admin_bot(message):

        if message.chat.id not in admin_id:
            return bot.send_message(message.chat.id, 'Нет прав')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        stop_parse_bt = types.KeyboardButton('📛 Остановить парсер')
        start_parse_bt = types.KeyboardButton('💹 Запустить парсер')
        markup.add(stop_parse_bt, start_parse_bt)
        bot.send_message(message.chat.id, 'Привет', reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def commands_admin(message):

        if message.chat.id not in admin_id:
            return bot.send_message(message.chat.id, 'Нет прав')

        if message.text == '📛 Остановить парсер':

            if not management.get_stop_parse():
                return bot.send_message(message.chat.id, f'Уже остановлен')

            management.set_stop_parse(False)
            bot.send_message(message.chat.id, f'Все парсеры остановлены')

        elif message.text == '💹 Запустить парсер':

            if management.get_stop_parse():
                return bot.send_message(message.chat.id, f'Уже запущен')

            management.set_stop_parse(True)

            start_threading([
                {"target": start_parse, "args": ((config("WB_URL_WOMAN_CLOTHES")), ("woman"),)},
                {"target": start_parse, "args": ((config("WB_URL_MEN_CLOTHES")), ("men"),)},
                {"target": start_parse, "args": ((config("WB_URL_CHILDREN_CLOTHES")), ("children"),)}
            ])

            bot.send_message(message.chat.id, f'Запущено')

        else:
            bot.send_message(message.chat.id, 'Нет такой команды')

    bot.polling(none_stop=True)
