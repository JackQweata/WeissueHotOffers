import asyncio
import re
import logging.config
import multiprocessing as mp

from modules.channel_object import ChannelObject
from modules.filtering_products import publication_post
from modules.publication_channel import publication_tg_channel
from modules.run_pyppeteer import run_pyppeteer
from src.OZON.product_card import CardProduct
from src.bots.admin.admin_message import send_message


class ParserManagementOzon(mp.Process):
    def __init__(self, channels):
        super().__init__()
        self._count_page = 1
        self._count_product = 0
        self._stop_parse = True
        self.__channels = channels
        self.__channel_name = channels.name
        self.__urls = channels.url

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.parser_run())

    async def parser_run(self):

        logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
        logger = logging.getLogger('sLogger')

        while self.stop_parse:
            try:
                for url in self.urls:
                    if not url.type:
                        continue

                    if self.count_page == 50:  # Ограничения по страницам
                        self.count_page = 1
                        continue
                    logger.info(f"{self.count_page} page {self.channel_name} (ozon)\n")

                    browser, page = await run_pyppeteer()
                    await page.goto(f"{url.name}{self.count_page}")
                    await asyncio.sleep(15)

                    elements = await page.querySelectorAll('div#paginatorContent > div > div > div')
                    for element in elements:
                        if not self.stop_parse:
                            break

                        element_title = await element.querySelector('div > a > span > span')
                        element_link = await element.querySelector('a')
                        element_price = await element.xpath('.//div[contains(text(), "₽")]')
                        element_img = await element.xpath('.//img[contains(@src, ".jpg")]')
                        element_remaining_product = await element.xpath('.//span[contains(text(), "Осталось")]')

                        if not (element_price or element_img or element_link):
                            continue

                        link_text = await page.evaluate('(element) => element.href', element_link)
                        product_id = re.search(r'-(\d+)/\?', link_text)
                        if not product_id:
                            continue
                        title = await page.evaluate('(element) => element.textContent', element_title)
                        product_price = await page.evaluate('(element) => element.textContent', element_price[0])
                        product_price_last = await page.evaluate('(element) => element.textContent', element_price[1])
                        price_style = await page.evaluate('(element) => element.style', element_price[0])
                        photo = await page.evaluate('(element) => element.src', element_img[0])
                        remaining_product = [] if not element_remaining_product else [
                            await page.evaluate('(element) => element.textContent',
                                                element_remaining_product[0])]

                        product_price = int(product_price.replace('\u2009', '').split('₽')[0])
                        product_price_last = int(product_price_last.replace('\u2009', '').split('₽')[0])
                        if product_price > 1500 and \
                                not price_style.get('2'):
                            continue

                        product_id = product_id.group(1)
                        is_publication_post = publication_post(product_id, product_price, link_text)
                        if not is_publication_post:
                            continue

                        instance_product = CardProduct(self.channel_name, product_id, title,
                                                       product_price, photo, remaining_product,
                                                       link_text, product_price_last)
                        if not instance_product:
                            continue

                        publication_tg_channel(self.channels, instance_product, "OZON")
                        self.count_product += 1

                    await browser.close()
            except Exception as _err:
                logger.error(_err)
                send_message('err', _err)
            finally:
                self.count_page += 1

        send_message('info', f"Нашлось {self.count_product} товара в категории {self.channel_name} (OZON)")

    def stop_parser(self):
        self.stop_parse = False

    def run_parser(self):
        self.stop_parse = True

    @property
    def channels(self):
        return self.__channels

    @property
    def stop_parse(self):
        return self._stop_parse

    @property
    def count_page(self):
        return self._count_page

    @property
    def count_product(self):
        return self._count_product

    @property
    def channel_name(self):
        return self.__channel_name

    @property
    def urls(self):
        return self.__urls

    @count_page.setter
    def count_page(self, value):
        self._count_page = value

    @count_product.setter
    def count_product(self, value):
        self._count_product = value

    @stop_parse.setter
    def stop_parse(self, value):
        self._stop_parse = value
