from flask import Flask, render_template, abort
from db_init import db
import config
from utils.decorators import allow_ip


app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
@allow_ip
def index():
    return abort(404)


@app.route('/log')
@allow_ip
def log():
    db.execute(""" SELECT channels.name, channels.cr_tm FROM channels; """)
    return render_template('log.html', db_elements=db.fetchall())


# def parse_url_channels():
#     successfull = True
#     try:
#         driver.parse_url_channels()
#     except Exception as e:
#         successfull = False
#         send_email(exception=e)
#     finally:
#         print(successfull)
#         template, msg = message_for_email(successfull=successfull)
#         return render_template(template, **msg)
#
#
# @app.route('/parse_programs')
# @allow_ip
# def parse_programs():
#     successfull = True
#     try:
#         driver.parse_tv_programs()
#     except Exception as e:
#         successfull = False
#         send_email(exception=e)
#     finally:
#         print(successfull)
#         template, msg = message_for_email(successfull=successfull)
#         return render_template(template, **msg)

if __name__ == '__main__':
    app.run()
