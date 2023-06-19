import logging.config
from modules.filtering_products import publication_post
from src.WB.product_card import CardProduct
from modules.publication_channel import publication_tg_channel
from src.bots.admin.admin_message import send_message
from utils.api_request import response
import threading as mp


class ParserManagementWB(mp.Thread):
    def __init__(self, channels):
        super().__init__()
        self._count_page = 1
        self._count_product = 0
        self._stop_parse = True
        self.__channels = channels
        self._channel_name = channels.name
        self.__urls = channels.url

    def __repr__(self):
        return f"{self.__class__.__name__}({self.channel_name}, {self.stop_parse})"

    def run(self):

        logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
        logger = logging.getLogger('sLogger')
        send_message('info', f'Начался парсинг WB категории: {self.channel_name}')

        while self.stop_parse:
            try:
                for url in self.__urls:
                    if url.type:
                        continue

                    if self.count_page == 50:  # Ограничения по страницам
                        self.count_page = 1
                        continue

                    logger.info(f"{self.count_page} page {self.channel_name}\n")
                    data_response = response(f'{url.name}{self.count_page}')

                    if not data_response:
                        logger.error('Не получены товары')
                        send_message('err', data_response)
                        break

                    for product in data_response['data']['products']:
                        product_id = product.get('id')
                        product_price = product.get('salePriceU')

                        if not self.stop_parse:
                            logger.info("Парсер остановлен через бота")
                            break

                        if product_price >= 15_000:
                            continue

                        link_product = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx"
                        is_publication_post = publication_post(product_id, product_price, link_product)
                        if not is_publication_post:
                            continue

                        instance_product = CardProduct(product, self.channel_name, link_product)
                        if not instance_product:
                            continue

                        publication_tg_channel(self.channels, instance_product, "WB")
                        self.count_product += 1

            except Exception as _err:
                logger.error(_err)
                send_message('err', _err)
            finally:
                self.count_page += 1

        send_message('info', f"Нашлось {self.count_product} товара в категории {self.channel_name} (WB)")

    def stop_parser(self):
        self.stop_parse = False

    def run_parser(self):
        self.stop_parse = True

    @property
    def stop_parse(self):
        return self._stop_parse

    @property
    def channels(self):
        return self.__channels

    @property
    def count_page(self):
        return self._count_page

    @property
    def count_product(self):
        return self._count_product

    @property
    def channel_name(self):
        return self._channel_name

    @stop_parse.setter
    def stop_parse(self, value):
        self._stop_parse = value

    @count_page.setter
    def count_page(self, value):
        self._count_page = value

    @count_product.setter
    def count_product(self, value):
        self._count_product = value
