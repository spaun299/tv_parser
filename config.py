import os


def database_url():
    db_url = os.environ['OPENSHIFT_POSTGRESQL_DB_URL'] if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else \
        'postgresql://admin:1111@localhost:5432/yandex'

    return db_url

SQLALCHEMY_DATABASE_URI = database_url()
DEBUG = True
MAIL_USERNAME = 'tvparser.in.ua@gmail.com'
MAIL_PASSWORD = 'dlvbcbj323~sdaf13d0dssfdfd'
