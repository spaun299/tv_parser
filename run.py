from parser_app.parser import SeleniumWebDriver
from flask import Flask, render_template
from utils.send_email import SendEmail
import config


driver = SeleniumWebDriver()
send_email = SendEmail().send_email
app = Flask(__name__)
app.config.from_object(config)


@app.route('/parse_url_channels')
def parse_url_channels():
    try:
        driver.parse_url_channels()
        return render_template('log.html', message='Successful')
    except Exception as e:
        send_email(exception=e)
        return render_template('log.html', message='Error, see email')


@app.route('/parse_programs')
def parse_programs():
    try:
        driver.parse_tv_programs()
        return render_template('log.html', message='Successful')
    except Exception as e:
        send_email(exception=e)
        return render_template('log.html', message='Error, see email')

if __name__ == '__main__':
    app.run()
