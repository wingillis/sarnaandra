import os
import glob
import datetime
import shutil


def initiate_watched_folders(db):
    '''Gets all watched folders and their associated
    experiments and begins to look for new files'''
    folders = db.get_watched_folders()
    return


def parse_file(path):
    pass


def check_watched_files(path, experiment, padding_time, move_path):
    files = glob.glob(os.path.join(path, '*'))
    now = datetime.datetime.now()
    td = datetime.timedelta(minutes=padding_time)
    if not os.path.exists(move_path):
        os.makedirs(move_path)
    for f in files:
        t = os.path.getmtime(f)
        t = datetime.datetime.fromtimestamp(t)
        if (now - td) > t:
            # do whatever here now
            print('Moving file to {0}'.format(move_path))
            shutil.move(f, move_path)
