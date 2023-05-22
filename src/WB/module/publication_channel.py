from decouple import config
from telebot import types

from src.WB.filtering_products import get_product_description


def publication_tg_channel(channel_type, card_product):
    dictionary_types = {
        "WOMAN": config("SELL_GROUP_WOMAN"),
        "MEN": config("SELL_GROUP_MEN"),
        "CHILDREN": config("SELL_GROUP_CHILDREN")
    }

    channel_id = dictionary_types[channel_type]

    name = card_product.name
    price = round(card_product.price / 100)
    brand = card_product.brand
    url_photo = card_product.image
    description = get_product_description(card_product)
    link_product = f"https://www.wildberries.ru/catalog/{card_product.product_id}/detail.aspx"

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти", url=link_product))

    text_post = f"{description}\n{name}\nБренд: {brand}\nЦена: {price}₽"
    return channel_id, url_photo, text_post, keyboard
