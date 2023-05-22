from threading import Lock


class ParserManagementWB:
    stop_parse = True

    def __init__(self):
        self._count_page = 1
        self._count_product = 0
        self._channel_type = None

    @property
    def count_page(self):
        return self._count_page

    @property
    def count_product(self):
        return self._count_product

    @property
    def channel_type(self):
        return self._channel_type

    @count_page.setter
    def count_page(self, value):
        self._count_page = value

    @count_product.setter
    def count_product(self, value):
        self._count_product = value

    @channel_type.setter
    def channel_type(self, value):
        self._channel_type = value


def set_stop_parse(value: bool):
    with Lock():
        ParserManagementWB.stop_parse = value
