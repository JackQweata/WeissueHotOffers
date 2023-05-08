from src.WB.filtering_products import product_search, get_product_description
from src.WB.module.parser_management import ParserManagementWB
from src.bots.admin.admin_message import send_message
from utils.api_request import response


def start_parse(URL, channel_type):
    send_message('info', f'Начался парсинг WB категории: {channel_type}')
    management = ParserManagementWB()
    count_page = management.get_count_page()

    while management.get_stop_parse():
        try:

            print(f"================= {count_page} page {channel_type} =================\n")
            data_response = response(f'{URL}{count_page}')

            if not data_response:
                print(data_response)
                send_message('err', data_response)
                break

            if count_page == 50:  # Ограничения по страницам
                management.set_count_page(1)
                break

            products = product_search(data_response['data']['products'])
            management.set_count_product(len(products))

            for product in products:
                description = get_product_description(product)

        except Exception as _err:
            print(_err)
            send_message('err', _err)
            continue
        finally:
            management.set_count_page(count_page + 1)

    send_message('info', f"Нашлось {len(management.get_count_product())} товара в категории {channel_type}")
