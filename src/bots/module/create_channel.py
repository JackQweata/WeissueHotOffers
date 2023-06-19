from modules.channel_object import ChannelObject


class NewCreateChannel(ChannelObject):
    def __init__(self, name='не установлено', channel_id='не установлено',
                 price='не установлено', description='не установлено', url='не установлено'):

        super().__init__(name, channel_id, price, description, url)
        self._name = name
        self._description = description
        self._price = price
        self._url = []
        self._channel_id = channel_id

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name, self.price})'

    def dict_item(self):
        return {"Название": self._name, "Цена": self._price, "url": self.url,
                "Описание": self._description, 'ID канала': self._channel_id}

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def price(self):
        return self._price

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def url(self):
        return self._url

    @name.setter
    def name(self, value):
        if value[0] == '\n':
            value = value[1:]
        self._name = value

    @description.setter
    def description(self, value):
        if value[0] == '\n':
            value = value[1:]
        self._description = value

    @price.setter
    def price(self, value):
        if value[0] == '\n':
            value = value[1:]
        self._price = int(value)

    @url.setter
    def url(self, value):
        self._url.append(value)

    @channel_id.setter
    def channel_id(self, value):
        self._channel_id = int(value)
