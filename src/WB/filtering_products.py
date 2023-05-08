from src.WB.module.parser_management import ParserManagementWB
from src.WB.module.product_card import CardProduct


def product_search(products: list):
    """Перибирает 100 товаргов на страеце и фильрует (1)"""

    card_product = []
    management = ParserManagementWB()

    for card in products:

        if not management.get_stop_parse():
            print("Парсер остановлен через бота")
            break
        elif card.get('salePriceU') >= 300_000:
            continue

        card_product.append(CardProduct(card.get('id'), card.get('salePriceU')))

    return card_product


def get_product_description(card_product):
    """ Получить опсиния для товара """

    type_title = None

    if not card_product.get_size_name():
        if card_product.get_price() >= card_product.get_last_price():
            return
        type_title = "Низкая цена"
    else:
        name_size = card_product.get_size_name()[0]
        type_title = f"Осталось мало штук\n {name_size} размера"

    return type_title
