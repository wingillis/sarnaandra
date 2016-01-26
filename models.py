from peewee import *
from app import db

# from the peewee docs
# Because we have not specified a primary key, peewee will
# automatically add an auto-incrementing integer primary key
# field named id.


class Base(Model):
    class Meta:
        database = db

class Experiment(Base):
    # this now also has a key called folders to associate
    # all the watched folders with it
    name = CharField()
    date_begin = DateTimeField()
    date_end = DateTimeField(null=True)
    tags = TextField(null=True)
    starred = BooleanField(default=False)
    description = TextField(null=True)


class Folder(Base):
    experiment = ForeignKeyField(Experiment, related_name='folders')
    interval = IntegerField() # in seconds
    path = CharField()


class Settings(Base):

    key = CharField()
    value = TextField()
    # suggested values include: backup path
    # folder structure


def create_tables():
    db.create_tables([Experiment, Folder, Settings], safe=True)
