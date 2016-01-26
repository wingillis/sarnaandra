import os
from os.path import join, expanduser

def get_path():
    default_path = join(expanduser('~'), 'sarnaandra')
    if not os.path.exists(default_path):
        os.makedirs(default_path)

    return join(default_path, 'metadata.db')

def setupDB():
    try:
        from models import *
        with opendb():
            db.create_tables([Experiment, Folder, Settings])
    except Exception as e:
        print(e)
        raise e
