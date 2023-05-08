from decouple import config
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, DateTime, func
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
    channel_id = Column(BigInteger)
    subscription_dates = Column(DateTime, server_default=func.now())
    end_subscription = Column(DateTime)


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    product_id = Column(BigInteger)
    price = Column(Integer)
    date = Column(DateTime, server_default=func.now())


Base.metadata.create_all(engine)
