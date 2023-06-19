
class CardProduct:
    def __init__(self, channel_name, product_id, name, price, img, size, link_product, price_last):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._brand = ''
        self._channel = channel_name
        self._image = img
        self._last_price = price_last
        self._size_name = size
        self._link_product = link_product
        self._description_text = None
        self._description_type = None

    def description(self):
        description_post = ''

        if not self.size_name:
            if self.price <= self.last_price:
                description_post = "ℹ️ Снижение цены \n\n"
                self._description_text = round(100 - (self.price * 100 / self.last_price), 1)
                self._description_type = 'salle'
        else:
            description_post = f"ℹ️ {self.size_name[0]}\n\n"
            self._description_type = 'size'

        return description_post

    @property
    def link_product(self):
        return self._link_product

    @property
    def last_price(self):
        return self._last_price

    @property
    def image(self):
        return self._image

    @property
    def size_name(self):
        return self._size_name

    @property
    def price(self):
        return self._price

    @property
    def name(self):
        return self._name

    @property
    def product_id(self):
        return self._product_id

    @property
    def brand(self):
        return self._brand

    @property
    def description_text(self):
        return self._description_text

    @property
    def description_type(self):
        return self._description_type

    @property
    def channel(self):
        return self._channel

    def __repr__(self):
        return f"{self.__class__.__name__}({self.product_id}, {self.price})"
