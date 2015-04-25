import os
from peewee import *

db_path = os.path.join(os.path.expanduser('~'), 'data_management.db')

db = SqliteDatabase(db_path)


class Base(Model):
    class Meta:
        database = db


class Experiment(Base):

    date_begin = DateTimeField()
    date_end = DateTimeField()
    file_filter = CharField()
    name = CharField()
    ordering = CharField()
    scripts_exist = BooleanField()


class WatchedFolder(Base):

    path = CharField()
    experiment_id = ForeignKeyField(Experiment,
                                    related_name='experiment_folders')
    check_interval = IntegerField()  # interval in seconds
    preserve_folder_structure = BooleanField()


class Settings(Base):

    key = CharField()
    value = CharField()


class Scripts(Base):

    filename = CharField()
    path = CharField()
    script_type = CharField()
    runtime_interval = IntegerField()  # interval in seconds
    tooltip = TextField()


class Files(Base):

    file_name = CharField()
    file_path = CharField()  # make sure that this is new, moved path
    file_type = CharField()
    associated_figures = TextField()
    starred = BooleanField()
    experiment_id = ForeignKeyField(Experiment, related_name='experiment')


class ExperimentScripts(Base):

    file_path = CharField()  # make sure it is moved path (copied file)
    experiment_id = ForeignKeyField(Experiment, related_name='experiment')
    save_raw_data = BooleanField()
    save_processed_data = BooleanField()
    file_filter = CharField()
