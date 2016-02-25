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
    db_elements = GetRecordsFromDb.get_full_channels_info()
    return render_template('log.html', db_elements=db_elements)

if __name__ == '__main__':
    app.run()
