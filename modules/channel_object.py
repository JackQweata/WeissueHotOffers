from ast import literal_eval
from sqlalchemy.orm import sessionmaker
from utils.mysql import engine, Channel, ChannelUrl
from threading import Lock


class ChannelObject:
    with Lock():
        channels_dict = {}

    def __init__(self, name, channel_id, price, description, url):
        self.__name = name
        self.__channel_id = channel_id
        self.__price = price
        self.__description = description
        self.__types_parsers = None
        self.__url = url

    @classmethod
    def collect_data(cls):
        Session = sessionmaker(bind=engine)
        session = Session()
        with session:
            channels = session.query(Channel).all()
            for channel in channels:
                types_parsers = [type_parser.type for type_parser in channel.url]
                type_parser = 3 if 1 in types_parsers and 0 in types_parsers else types_parsers[0]
                cls.channels_dict[channel.name] = {
                    "class": ChannelObject(channel.name, channel.channel_id, channel.price, channel.description,
                                           channel.url),
                    "type": type_parser,
                    "status": True,
                    }

    def create_new_channel(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        with session:
            new_channel = Channel(name=self.name, description=self.description,
                                  price=self.price, channel_id=self.channel_id)

            for url_item in self.url.values():
                url = ChannelUrl(name=url_item['url'], type=url_item['type'])
                new_channel.url.append(url)

            session.add(new_channel)
            session.commit()

    @property
    def name(self):
        return self.__name

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def price(self):
        return self.__price

    @property
    def description(self):
        return self.__description

    @property
    def types_parsers(self):
        return self.__types_parsers

    @property
    def url(self):
        return self.__url

    def __str__(self):
        return self.__name
