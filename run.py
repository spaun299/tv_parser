from flask import Flask, render_template, abort
import config
from utils.decorators import allow_ip
from parser_app.models import GetRecordsFromDb
from utils.log import write_to_log

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
@allow_ip
def index():
    return abort(404)


@app.route('/log')
@allow_ip
def log():
    write_to_log('sss')
    channels_log = GetRecordsFromDb.get_last_log_info('channels')
    programs_log = GetRecordsFromDb.get_last_log_info('tv_programs')
    db_elements = GetRecordsFromDb.get_full_channels_info()
    return render_template('log.html', db_elements=db_elements,
                           channels_log=channels_log, programs_log=programs_log)


if __name__ == '__main__':
    app.run()
