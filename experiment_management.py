import os
import glob
import datetime
import shutil
import toolz
import functools
import helpers
import main
import importlib
import itertools
import sys

def check_watched_files(path, experiment, padding_time, move_path, ordering, watched_folder_id):
    files = glob.glob(os.path.join(path, '*'))
    now = datetime.datetime.now()
    td = datetime.timedelta(minutes=padding_time)
    if not os.path.exists(move_path):
        os.makedirs(move_path)
    main._db_connect()
    scripts = list(main.ExperimentScripts.select().where(main.ExperimentScripts.watched_folder_id == watched_folder_id))
    print(len(scripts))
    for f in files:
        try:
            t = os.path.getmtime(f)
            t = datetime.datetime.fromtimestamp(t)
            fpath, ext = os.path.splitext(f)
            fname = os.path.basename(f)
            if (now - td) > t:
                # do whatever here now
                ext = ext[1:]
                path = generate_file_path(move_path, experiment, ordering, ext)
                assoc_figs = []
                for script in scripts:
                    if script.file_filter == ext:
                        fp = put_in_path(script.file_path)
                        sc = importlib.import_module(fp)
                        newfilepaths = sc.run(f)
                        if type(newfilepaths) is not str:
                            pps = itertools.chain(*newfilepaths)
                            [assoc_figs.append(ps) for ps in pps]
                        else:
                            assoc_figs.append(newfilepaths)
                imgpath = os.path.join(path, 'images')
                if not os.path.exists(imgpath):
                    os.makedirs(imgpath)
                save_img_paths = []
                for p in assoc_figs:
                    newpath = move_or_change_name(p, imgpath)
                    save_img_paths.append(newpath)

                main.Files.create(file_name=fname, file_path=path, file_type=ext, discovered_date=datetime.datetime.now(), starred=False, experiment_id=main.Experiment.get(main.Experiment.name == experiment).id, associated_figures=','.join(save_img_paths))
                if path:
                    if os.path.exists(path):
                        shutil.move(f, path)
                    else:
                        os.makedirs(path)
                        shutil.move(f, path)
                else:
                    print('Error, path did not work')
        except OSError as e:
            print(e)

    main._db_close(' ')


def move_or_change_name(path, newpath):
    base = os.path.basename(path)
    file_name, ext = os.path.splitext(base)
    counter = -1

    def tp(fname, ext, p, c=None):
        if type(c) is not type(None):
            return os.path.join(p, (fname + str(c) + ext))
        else:
            return os.path.join(p, (fname + ext))
    temp_path = tp(file_name, ext, newpath)
    while os.path.exists(temp_path):
        counter += 1
        temp_path = tp(file_name, ext, newpath, counter)

    shutil.move(path, temp_path)
    return temp_path


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


def put_in_path(fpath):
    p, f = os.path.split(fpath)
    if fpath not in sys.path:
        sys.path.append(p)
    f, e = os.path.splitext(f)
    return f