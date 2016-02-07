import datetime
from parser_app.parser import SeleniumWebDriver
from apscheduler.schedulers.background import BackgroundScheduler
import time
from utils.decorators import execution_time
driver = SeleniumWebDriver()
from flask import Flask
from utils.email import SendEmail

app = Flask(__name__)
send_email = SendEmail().send_email


@app.route('/parse_url_channels')
def parse_url_channels():
    try:
        driver.parse_url_channels()
    except Exception as e:
        send_email(exception=e)


@app.route('/parse_programs')
def parse_programs():
    try:
        driver.parse_tv_programs()
    except Exception as e:
        send_email(exception=e)

if __name__ == '__main__':
    app.run()
