import requests
from notify.config import SLACK_URL
import json


class Slack:

	def __init__(self):
		"""
		this is the initialization of the slack class to push all messages the general slack channel.
		"""
		self.headers = {'Content-type': 'application/json'}
		self.data = {
			"text": "",
			"attachments": []
		}

	def add_data(self, prop, val):
		self.data[prop] = val
		pass

	def create_attachment(self, data):
		"""
		:return: Ideally return a new attachment to be appended to main slack message data.
		"""
		self.data['attachments'].append(data)

	def send(self, message=None):
		if not message:
			message = self.data
		return requests.post(SLACK_URL, data=json.dumps(message), headers=self.headers)

	def __call__(self, *args, **kwargs):
		return self.data

	def __repr__(self):
		return str(self.data)
