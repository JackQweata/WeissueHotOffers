from decouple import config
from src.WB.run_parser import start_parse


def test_run_parse():
    assert start_parse(config('WB_URL_CHILDREN_CLOTHES'), "children") == 1