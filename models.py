import os
from manager import get_path
from peewee import *
from contextlib import contextmanager

db = SqliteDatabase(get_path())

# from the peewee docs
# Because we have not specified a primary key, peewee will
# automatically add an auto-incrementing integer primary key
# field named id.

@contextmanager
def opendb():
    db.connect()
    yield
    db.close()

class Base(Model):
    class Meta:
        database = db

class Experiment(Base):
    # this now also has a key called folders to associate
    # all the watched folders with it
    name = CharField()
    date_begin = DateTimeField()
    date_end = DateTimeField()
    tags = TextField()
    starred = BooleanField()
    description = TextField()


class Folder(Base):
    experiment = ForeignKeyField(Experiment, related_name='folders')
    interval = IntegerField() # in seconds
    path = CharField()


class Settings(Base):

    key = CharField()
    value = TextField()
    # suggested values include: backup path
    # folder structure
