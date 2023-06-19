from modules.run_chromedriver import get_chromedriver
from modules.xpath_element import exception_element
from utils.api_request import response


class CardProduct:
    def __init__(self, product, channel, link_product):
        self._product_id = product.get('id')
        self._name = product.get('name')
        self._price = round(product.get('salePriceU') / 100)
        self._brand = product.get('brand')
        self._channel = channel
        self._image = None
        self._last_price = 0
        self._size_name = []
        self._description_text = None
        self._description_type = None
        self._link_product = link_product

        driver = get_chromedriver()
        driver.get(f'https://www.wildberries.ru/catalog/{self.product_id}/detail.aspx')
        get_image = exception_element(driver, '//img[contains(@src,"big/1.jpg")]')
        if not get_image:
            return
        self._image = get_image.get_attribute('src')
        driver.quit()

    def description(self):
        description_post = ''

        if not self.size_name:
            if self.price <= self.last_price:
                description_post = "ℹ️ Снижение цены \n\n"
                self._description_text = round(100 - (self.price * 100 / self.last_price), 1)
                self._description_type = 'salle'
        else:
            description_post = f"ℹ️ Осталось мало штук размера: \n" + ', '.join(self._size_name) + '\n\n'
            self._description_type = 'size'

        return description_post

    @property
    def last_price(self):
        if self.image:
            url_histore_price = self.image.replace('images/big/1.jpg', 'info/price-history.json')
            histore_price = response(url_histore_price)
            if histore_price:
                self._last_price = round(histore_price[-1]["price"]["RUB"] / 100)

        return self._last_price

    @property
    def image(self):
        return self._image

    @property
    def size_name(self):
        sizes = response(f'https://card.wb.ru/cards/detail?dest=-1257786&nm={self._product_id}')
        if not sizes:
            return self._size_name

        sizes_name = sizes["data"]["products"][0]
        for item in sizes_name["sizes"]:
            if item["stocks"] and item["stocks"][-1]["qty"] <= 3 and len(self._size_name) <= 3:
                self._size_name.append(item["name"])

        return self._size_name

    @property
    def link_product(self):
        return self._link_product

    @property
    def price(self):
        return self._price

    @property
    def name(self):
        return self._name

    @property
    def product_id(self):
        return self._product_id

    @property
    def brand(self):
        return self._brand

    @property
    def description_text(self):
        return self._description_text

    @property
    def description_type(self):
        return self._description_type

    @property
    def channel(self):
        return self._channel

    def __repr__(self):
        return f"{self.__class__.__name__}({self.product_id}, {self.price})"
