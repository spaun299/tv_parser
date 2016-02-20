from parser_app.parser import SeleniumWebDriver
from flask import Flask, render_template
from utils.send_email import SendEmail
from utils.messages import message_for_email
import config
from utils.decorators import allow_ip


driver = SeleniumWebDriver()
send_email = SendEmail().send_email
app = Flask(__name__)
app.config.from_object(config)


@app.route('/parse_url_channels')
@allow_ip
def parse_url_channels():
    successfull = True
    try:
        driver.parse_url_channels()
    except Exception as e:
        successfull = False
        send_email(exception=e)
    finally:
        print(successfull)
        template, msg = message_for_email(successfull=successfull)
        return render_template(template, **msg)


@app.route('/parse_programs')
@allow_ip
def parse_programs():
    successfull = True
    try:
        driver.parse_tv_programs()
    except Exception as e:
        successfull = False
        send_email(exception=e)
    finally:
        print(successfull)
        template, msg = message_for_email(successfull=successfull)
        return render_template(template, **msg)

if __name__ == '__main__':
    app.run()
