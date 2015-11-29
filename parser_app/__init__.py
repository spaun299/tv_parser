from flask import Flask, g
import config
from parser_app.parser import SeleniumWebDriwer
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.ext.declarative import declarative_base

parser = SeleniumWebDriwer()


def init_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.before_request(db_session)
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(parser.run, 'interval', seconds=1)
    scheduler.start()
    return app


def db_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    g.sql_connection = engine.connect()
    g.db_session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=engine))
