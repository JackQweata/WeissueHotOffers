from modules.run_chromedriver import get_chromedriver
from modules.xpath_element import exception_element
from selenium.webdriver.common.by import By

from utils.api_request import response


class CardProduct:
    def __init__(self, product_id, price):
        self.product_id = product_id
        self.driver = get_chromedriver()
        self.image = None
        self.last_price = 0
        self.size_name = []
        self.price = price

    def get_last_price(self):
        if self.image:
            url_histore_price = self.image.replace('images/big/1.jpg', 'info/price-history.json')
            histore_price = response(url_histore_price)
            if not histore_price:
                self.last_price = histore_price[-1]["price"]["RUB"]

        return self.last_price

    def get_image(self):
        self.driver.get(f'https://www.wildberries.ru/catalog/{self.product_id}/detail.aspx')

        get_image = exception_element(self.driver, '//div[@class="zoom-image-container"]/img')
        self.image = get_image.get_attribute('src')
        self.driver.quit()

        return self.image

    def get_size_name(self):
        sizes_name = response(f'https://card.wb.ru/cards/detail?dest=-1257786&nm={self.product_id}')
        if not sizes_name:
            return self.size_name

        sizes_name = sizes_name["data"]["products"][0]

        for item in sizes_name["sizes"]:
            if item["stocks"] and item["stocks"][-1]["qty"] <= 5:
                self.size_name.append(item["name"])

        return self.size_name

    def get_price(self):
        return self.price
