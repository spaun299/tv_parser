from flask import Flask, g
import config
from parser_app.parser import SeleniumWebDriwer
from apscheduler.schedulers.background import BackgroundScheduler

parser = SeleniumWebDriwer()


def init_app():
    app = Flask(__name__)
    app.config.from_object(config)
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(parser.run, 'interval', seconds=1)
    scheduler.start()
    return app
