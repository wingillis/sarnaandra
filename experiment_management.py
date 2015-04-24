import os
import glob
import datetime
import shutil
import toolz
import functools
import helpers


def check_watched_files(path, experiment, padding_time, move_path, db):
    files = glob.glob(os.path.join(path, '*'))
    now = datetime.datetime.now()
    td = datetime.timedelta(minutes=padding_time)
    ordering = helpers.get_ordering(experiment, db)
    if not os.path.exists(move_path):
        os.makedirs(move_path)
    for f in files:
        try:
            t = os.path.getmtime(f)
            t = datetime.datetime.fromtimestamp(t)
            fpath, ext = os.path.splitext(f)
            if (now - td) > t:
                # do whatever here now
                ext = ext[1:]
                path = generate_file_path(move_path, experiment, ordering, ext)
                if path:
                    print('Moving file to {0}'.format(path))
                    if os.path.exists(path):
                        shutil.move(f, path)

                    else:
                        print('Making directory tree: {0}'.format(path))
                        os.makedirs(path)
                        shutil.move(f, path)
                else:
                    print('Error, path did not work')
        except OSError as e:
            os.remove(f)
            print('Removing {0} because of symlink problem'.format(f))



def generate_file_path(backup_location, exp, ordering, file_type):
    ''':params backup location, experiment, ordering, file_type
    :return folder path for where the file can be stored'''
    ordering_funcs = {'date': helpers.get_date, 'file_type': lambda: file_type,
                      'experiment': lambda: exp,
                      'backup_location': lambda: backup_location
                      }
    order = [ordering_funcs[val] for val in ordering]
    path = functools.reduce(os.path.join, map(lambda a: a(), order))
    return path
