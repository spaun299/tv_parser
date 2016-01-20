from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer
import datetime
import pytz


Base = declarative_base()


def get_current_datetime(timezone='Europe/Moscow'):
    dt = datetime.datetime.now(pytz.timezone(timezone))
    return datetime.datetime(dt.year, dt.month, dt.day, hour=dt.hour, minute=dt.minute)


class ChannelLink(Base):
    __tablename__ = 'channel_link'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    name = Column(String(200), nullable=False, unique=True)
    url = Column(String(500), nullable=False, unique=True)
    language = Column(String(2), default='ru')
    md_tm = Column(DateTime, default=get_current_datetime())

    def __init__(self, name=None, url=None, language='ru'):
        self.name = name
        self.url = url
        self.language = language


class ParserInfo(Base):
    __tablename__ = 'parser_info'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    main_url = Column(String(200), nullable=False)

    def __init__(self, main_url=None):
        self.main_url = main_url
