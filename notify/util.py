
__all__ = ['SQLite']
from .db_util import db_connect, redis_connect
from config import SQLITE_DB


class SQLite:

	# get and initialize the database connection with config DB.
	con = db_connect(SQLITE_DB)

	# get the cursor for writing and reading to the database.
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

	dbs = ['kith', 'nike', 'yeezy', 'adidas', 'rise', 'addict', 'nicekicks']

	def create_tables(self):
		try:
			# execute the creation of this table
			for i in self.dbs:
				self.cursor.execute(self.sql_format_create.format(i))
			return self.cursor
		except Exception as err:
			print(err)

	def insert_data(self, table, name, price, image, link, date):
		try:
			sql = self.sql_format_insert.format(table=table, name=name, price=price, image=image, link=link, date=date)
			self.cursor.execute(sql)
			self.con.commit()
			return 'Done'
		except Exception as err:
			print(err.with_traceback(None))
			return None

	def select_data(self, table):
		try:
			self.cursor.execute(self.sql_format_select.format(table))
			return self.cursor.fetchall()
		except Exception as err:
			print('this error is from selecting')
			print(err)


class Redis:

	redis = redis_connect()

	def push(self, prop, val):
		return self.redis.lpush(prop, val)

	def pull(self, prop):
		return self.redis.lrange(prop, 0, -1)

	def add(self, prop, data):
		return self.redis.sadd(prop, "{} {}".format(data['link'], data['image']))

	def __call__(self, *args, **kwargs):
		return self.redis
