import os
from peewee import *

db_path = os.path.join(os.path.expanduser('~'), 'data_management.db')

db = SqliteDatabase(db_path)


class Base(Model):
    class Meta:
        database = db


class Experiment(Base):
    # __tablename__ = 'experiments'

    id = IntegerField(primary_key=True)
    date_begin = DateTimeField()
    date_end = DateTimeField()
    file_filter = CharField()
    name = CharField()
    # folder_paths = Column(String)


class Watched_Folder(Base):
    # __tablename__ = 'watched_folders'

    id = IntegerField(primary_key=True)
    path = CharField()
    experiment_id = ForeignKeyField(Experiment,
                                    related_name='experiment_folders')
    check_interval = IntegerField()  # interval in seconds
    # experiment = relationship(Experiment)


class Settings(Base):
    # __tablename__ = 'settings'

    key = CharField()
    value = CharField()


class Scripts(Base):
    # __tablename__ = 'scripts'

    id = IntegerField(primary_key=True)
    filename = CharField()
    path = CharField()
    script_type = CharField()
    runtime_interval = IntegerField()  # to measure interval in seconds
    tooltip = TextField()
