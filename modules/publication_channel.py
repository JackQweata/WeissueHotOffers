import logging.config
from time import sleep
from decouple import config
from telebot import types, TeleBot
from modules.editing_preview import creating_frame


def publication_tg_channel(channels, card_product, tags):
    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
    logger = logging.getLogger('sLogger')

    bot = TeleBot(config("TOKEN_BOT_GROUP"))
    name = card_product.name
    price = card_product.price
    brand = f"✅ {card_product.brand}\n\n" if card_product.brand else card_product.brand
    description = card_product.description()
    url_photo = creating_frame(card_product, tags)
    link_product = card_product.link_product

    logger.info(f'--------\n{name}\n{card_product.product_id}\n--------\n')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти", url=link_product))
    text_post = f"\n✨ {name} ✨\n" + brand + description + f"📉 {price}₽\n"

    bot.send_photo(channels.channel_id, url_photo, caption=text_post, reply_markup=keyboard)
    sleep(180)
