from decouple import config
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, DateTime, func, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

user = config("bd_user")
password = config("bd_passwd")
host = config("bd_host")
database = config("bd_database")
port = 3306

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    user_id = Column(BigInteger)
    subscriptions = relationship('UserSubscriptions', backref='user')


class UserSubscriptions(Base):
    __tablename__ = 'user_subscriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(50))
    channel_id = Column(BigInteger)
    subscription_dates = Column(DateTime, server_default=func.now())
    end_subscription = Column(DateTime)


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    product_id = Column(BigInteger)
    price = Column(Integer)
    url = Column(Text)
    date = Column(DateTime, server_default=func.now())


class Channel(Base):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, default='')
    price = Column(Integer, nullable=False)
    url = relationship('ChannelUrl', backref='channel')
    channel_id = Column(BigInteger, nullable=False)


class ChannelUrl(Base):
    __tablename__ = 'channel_url'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    channel_id = Column(Integer, ForeignKey('channel.id'))
    type = Column(Integer, nullable=False)


Base.metadata.create_all(engine)
