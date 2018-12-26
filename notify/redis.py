from redis import Redis


class Redix:

	def __init__(self, host, port, db):
		self.redis = Redis(host=host, port=port, db=db)

