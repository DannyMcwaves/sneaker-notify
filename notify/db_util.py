# db_utils.py
import os
import sqlite3
import redis

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')


def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con


def redis_connect():
    """
    this connection based protocol is for redis and is to be used for key based data storage.
    :return:
    """
    return redis.Redis(host='localhost', port=6379, db=0)
