from decouple import config
from telebot import TeleBot
import logging.config
from src.WB.filtering_products import product_search, get_product_description, published_posts
from src.WB.module.parser_management import ParserManagementWB
from src.WB.module.publication_channel import publication_tg_channel
from src.bots.admin.admin_message import send_message
from utils.api_request import response


def start_parse(URL, channel_type):
    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
    logger = logging.getLogger('sLogger')

    send_message('info', f'Начался парсинг WB категории: {channel_type}')
    management = ParserManagementWB()

    while management.get_stop_parse():
        try:

            logger.info(f"{management.get_count_page()} page {channel_type}\n")
            data_response = response(f'{URL}{management.get_count_page()}')

            if not data_response:
                logger.error('Не получены товары')
                send_message('err', data_response)
                break

            if management.get_count_page() == 50:  # Ограничения по страницам
                break

            products = product_search(data_response['data']['products'])

            for product in products:

                if not management.get_stop_parse():
                    logger.info("Парсер остановлен через бота")
                    break

                is_published = published_posts(product)

                if not is_published:
                    continue

                bot = TeleBot(config("TOKEN_BOT_GROUP"))
                channel_id, url_photo, text_post, keyboard = publication_tg_channel(channel_type, product)
                bot.send_photo(channel_id, url_photo, caption=text_post, reply_markup=keyboard)

                management.set_count_product(len(products))

        except Exception as _err:
            logger.error(_err)
            send_message('err', _err)
            continue
        finally:
            management.set_count_page(management.get_count_page() + 1)

    send_message('info', f"Нашлось {management.get_count_product()} товара в категории {channel_type}")
