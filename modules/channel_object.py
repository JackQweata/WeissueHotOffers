from ast import literal_eval
from sqlalchemy.orm import sessionmaker
from utils.mysql import engine, Channel
from threading import Lock


class ChannelObject:
    with Lock():
        channels_dict = {}

    def __init__(self, name, channel_id, price, description, url):
        self.__name = name
        self.__channel_id = channel_id
        self.__price = price
        self.__description = literal_eval(description)
        self.__url = url

    @classmethod
    def collect_data(cls):
        Session = sessionmaker(bind=engine)
        session = Session()
        with session:
            channels = session.query(Channel).all()
            for channel in channels:
                channel_url = [url.name for url in channel.url]
                cls.channels_dict[channel.name] = {
                        "class": ChannelObject(channel.name, channel.channel_id, channel.price, channel.description,
                                               channel_url)}

    def __str__(self):
        return self.__name

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
    def url(self):
        return self.__url
