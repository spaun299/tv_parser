import config_app
import psycopg2
import psycopg2.extras

sql_connection = psycopg2.connect(config_app.POSTGRES_DATABASE_URI)
db = sql_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
