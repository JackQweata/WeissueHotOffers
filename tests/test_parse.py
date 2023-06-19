from decouple import config
from src.WB.run_parser import start_parse


def test_run_parse():
    assert start_parse(["https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&dest=-1257786&query=%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0%20%D0%B4%D0%BB%D1%8F%20%D0%B6%D0%B5%D0%BD%D1%89%D0%B8%D0%BD&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false&page="], "WOMAN") == 1