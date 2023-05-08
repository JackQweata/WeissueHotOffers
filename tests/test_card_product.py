from src.WB.module.product_card import CardProduct


def test_card_product():
    card = CardProduct(24695836)
    assert type(card.get_image()) == str
    assert len(card.get_size_name()) == 1
    assert type(card.get_price_history()) == int
