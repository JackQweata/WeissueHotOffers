import datetime
import logging
from src.WB.module.product_card import CardProduct
from sqlalchemy.orm import sessionmaker
from utils.mysql import engine, Posts


def product_search(products: list):
    """Перибирает 100 товаргов на страеце и фильрует (1)"""

    card_product = []

    for card in products:
        if card.get('salePriceU') >= 300_000:
            continue
        card_product.append(CardProduct(card))

    return card_product


def get_product_description(card_product):
    """ Получить опсиния для товара """

    type_title = ''

    if not card_product.size_name:
        if card_product.price <= card_product.last_price:
            type_title = "Низкая цена"
    else:
        name_size = card_product.size_name[0]
        type_title = f"Осталось мало штук\n {name_size} размера"

    return type_title


def published_posts(product):
    Session = sessionmaker(bind=engine)
    session = Session()

    with session:
        post = session.query(Posts).filter(Posts.product_id == product.product_id).first()

        if not post:
            session.add(Posts(product_id=product.product_id, price=product.price))
            session.commit()
            return True

        publication_life = post.date + datetime.timedelta(weeks=1)
        if post.price != product.price or datetime.datetime.now() > publication_life:
            session.delete(post)
            session.commit()
            return True
