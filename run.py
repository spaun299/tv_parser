from flask import Flask, render_template, abort
from db_init import db
import config
from utils.decorators import allow_ip
from parser_app.models import GetRecordsFromDb


app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
@allow_ip
def index():
    return abort(404)

@app.route('/log')
@allow_ip
def log():
    db.execute(""" SELECT c.name, c.cr_tm, c.link, c.web_site, c.description, f.file_link as icon_link FROM channels c LEFT JOIN files f ON c.icon_id=f.id; """)
    db_elements = GetRecordsFromDb.get_full_channels_info()
    return render_template('log.html', db_elements=db_elements)


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
