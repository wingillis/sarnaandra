import os
import glob
import datetime
import shutil
import toolz
import functools


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


def generate_file_path(backup_location, exp, ordering, file_type):
    ''':params backup location, experiment, ordering, file_type
    :return folder path for where the file can be stored'''
    ordering_funcs = {'date': get_date, 'file_type': lambda: file_type,
                      'experiment': lambda: exp,
                      'backup_location': lambda: backup_location,
                      ''}
    order = [ordering_funcs[val] for val in ordering]
    path = functools.reduce(os.path.join, map(lambda a: a(), order))
    if type(path) is str:
        return path
    else:
        print('Something is wrong with function generate_file_path, result not string')
        return False
