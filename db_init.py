import config
import psycopg2

connection = psycopg2.connect(config.POSTGRES_DATABASE_URI)
db = connection.cursor()
