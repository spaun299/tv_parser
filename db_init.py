import config
import psycopg2
import psycopg2.extras

sql_connection = psycopg2.connect(config.POSTGRES_DATABASE_URI)
db = sql_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
