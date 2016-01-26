import os
from flask import Flask
from contextlib import contextmanager
from os.path import join, expanduser
from peewee import SqliteDatabase

app = Flask(__name__, static_url_path='')

def get_path():
    default_path = join(expanduser('~'), 'sarnaandra')
    if not os.path.exists(default_path):
        os.makedirs(default_path)
    return join(default_path, 'metadata.db')

db = SqliteDatabase(get_path())

@contextmanager
def opendb():
    db.connect()
    yield
    db.close()
