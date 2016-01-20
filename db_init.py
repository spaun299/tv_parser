from sqlalchemy.ext.declarative import declarative_base
from flask import g
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import config
from parser_app.models import ChannelLink, ParserInfo
Base = declarative_base()


def db_query(arg, **kwargs):
    return db_session().query(arg).filter_by(**kwargs)


def db_session():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return db
