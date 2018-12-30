
__all__ = ['select_data', 'create_tables', 'insert_data']
from .db_util import db_connect
from config import SQLITE_DB


# Instantiate the database.
con = db_connect(SQLITE_DB)
cursor = con.cursor()


# Database SQL Statements.
sql_format_create = """
CREATE TABLE IF NOT EXISTS {} (
	name text NOT NULL,
	price text NOT NULL,
	image text NOT NULL UNIQUE,
	date DATE NOT NULL,
	link text NOT NULL UNIQUE
)
"""

sql_format_insert = """
INSERT INTO {table} (name, price, image, link, date) VALUES (\"{name}\", \"{price}\", \"{image}\", \"{link}\", \"{date}\")
"""

sql_format_select = """
SELECT name, price, image, link, date FROM {}
"""

kith_sql = sql_format_create.format('kith')
nike_sql = sql_format_create.format('nike')
yeezy_sql = sql_format_create.format('yeezy')
adidas_sql = sql_format_create.format('adidas')


def create_tables():
	try:
		# execute the creation of this table
		for i in [kith_sql, nike_sql, yeezy_sql, adidas_sql]:
			cursor.execute(i)
		return cursor
	except Exception as err:
		print(err)


def insert_data(table, name, price, image, link, date):
	try:
		sql = sql_format_insert.format(table=table, name=name, price=price, image=image, link=link, date=date)
		cursor.execute(sql)
		con.commit()
		return 'Done'
	except Exception as err:
		print(err)
		return None


def select_data(table):
	try:
		cursor.execute(sql_format_select.format(table))
		return cursor.fetchall()
	except Exception as err:
		print('this error is from selecting')
		print(err)
