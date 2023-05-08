from threading import Lock


class ParserManagementWB:
    def __init__(self):
        self.stop_parse = True
        self.count_page = 1
        self.count_product = 0

    def set_stop_parse(self, value: bool):
        with Lock():
            self.stop_parse = value

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
