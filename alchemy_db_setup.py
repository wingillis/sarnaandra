import os
import sys
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Experiments(Base):
    __tablename__ = 'experiments'

    id = Column(Integer, primary_key=True)
    date_begin = Column(Date, nullable=False)
    date_end = Column(Date)
    file_filter = Column(String)
    name = Column(String(250))
    # folder_paths = Column(String)


class Watched_Folder(Base):
    __tablename__ = 'watched_folders'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    check_interval = Column(Integer)  # interval in seconds
    experiment = relationship(Experiments)


class Settings(Base):
    __tablename__ = 'settings'

    key = Column(String)
    value = Column(String)


class Scripts(Base):
    __tablename__ = 'scripts'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    path = Column(String)
    script_type = Column(String)
    runtime_interval = Column(String)

db_path = os.path.expanduser('~') + 'data_management.db'
engine = create_engine('sqlite:///{0}'.format(db_path))

Base.metadata.create_all(engine)