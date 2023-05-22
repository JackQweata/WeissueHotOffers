from modules.run_chromedriver import get_chromedriver
from modules.xpath_element import exception_element
from selenium.webdriver.common.by import By

from utils.api_request import response


class CardProduct:
    def __init__(self, product):
        self._product_id = product.get('id')
        self._name = product.get('name')
        self._price = product.get('salePriceU')
        self._brand = product.get('brand')
        self._image = None
        self._last_price = 0
        self._size_name = []

    @property
    def last_price(self):
        if self.image:
            url_histore_price = self.image.replace('images/big/1.jpg', 'info/price-history.json')
            histore_price = response(url_histore_price)
            if not histore_price:
                self._last_price = histore_price[-1]["price"]["RUB"]

        return self._last_price

    @property
    def image(self):
        driver = get_chromedriver()
        driver.get(f'https://www.wildberries.ru/catalog/{self.product_id}/detail.aspx')
        get_image = exception_element(driver, '//div[@class="zoom-image-container"]/img')
        self._image = get_image.get_attribute('src')
        driver.quit()

        return self._image

    @property
    def size_name(self):
        sizes_name = response(f'https://card.wb.ru/cards/detail?dest=-1257786&nm={self._product_id}')
        if not sizes_name:
            return self._size_name

        sizes_name = sizes_name["data"]["products"][0]

        for item in sizes_name["sizes"]:
            if item["stocks"] and item["stocks"][-1]["qty"] <= 3:
                self.size_name.append(item["name"])

        return self._size_name

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
