from threading import Lock


class ParserManagementWB:
    stop_parse = True

    def __init__(self):
        self.count_page = 1
        self.count_product = 0
        self.channel_type = None

    def set_count_page(self, value):
        self.count_page = value

    def set_count_product(self, value):
        self.count_product = value

    def get_stop_parse(self):
        return self.stop_parse

    def get_count_page(self):
        return self.count_page

    def get_count_product(self):
        return self.count_product


def set_stop_parse(value: bool):
    with Lock():
        ParserManagementWB.stop_parse = value
