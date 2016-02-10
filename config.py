import os
import sys


def database_url():
    # db_url = os.environ['OPENSHIFT_POSTGRESQL_DB_URL'] if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else \
    #     'postgresql://admin:1111@localhost:5432/yandex'
    db_name = 'yandex'

    if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL'):
        host = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
        port = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']
        user = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
        password = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']
    else:
        host, port, user, password = 'localhost', '5432', 'admin', '1111'
    db_url = "host='{host}' dbname='{db_name}' port='{port}' user='{user}' password='{password}'".format(
        host=host, db_name=db_name, user=user, password=password, port=port
    )

    return db_url

POSTGRES_DATABASE_URI = database_url()
DEBUG = True
MAIL_USERNAME = 'tvparser.in.ua@gmail.com'
MAIL_PASSWORD = 'dlvbcbj323~sdaf13d0dssfdfd'
MAIN_PARSE_URL = 'https://tv.yandex.ua/187?grid=all&period=all-day'
ALLOWED_iPS = ['127.0.0.1']
