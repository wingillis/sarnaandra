import importlib
import os
import sys
import helpers
import experiment_management
import logging
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

__author__ = 'wgillis'


logging.basicConfig()


scheduler = None

running_scripts = {}


def begin():
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()


def set_up_folders(watched_folders, root_dir):
    # each index of watched_folders contains a tuple of the
    # folder location, recurrence time and experiment
    watched_folders = list(watched_folders)
    if watched_folders:
        for folder in watched_folders:
            ordering = folder.experiment_id.ordering.split(',')
            add_watched_folder(folder.path, folder.check_interval,
                               folder.experiment_id.name, root_dir, ordering, folder.id)
    else:
        print('Watched folders is empty. Maybe there is a new user')


def print_jobs():
    print('Printing get jobs')
    f = scheduler.get_jobs()
    for i in f:
        print(i)


def add_recurring_script(p, recurrence_time):
    '''adds a file (currently only python scripts)
        to be run once every recurrence_time (which is in seconds)'''
    if os.path.isfile(p):
        # scheduler.print_jobs()
        path, file = os.path.split(p)
        sys.path.append(path)
        library = importlib.import_module(file[:-3])
        print('Importing module {1} from {0}'.format(path, file))
        interval = IntervalTrigger(seconds=int(recurrence_time))
        if p not in running_scripts:
            running_scripts[p] = scheduler.add_job(library.run, interval)
        scheduler.print_jobs()
        return 0
    else:
        print('script does not exist at location\
               {0}\nadd file failed'.format(p))
        return 1


def add_watched_folder(path, check_interval, experiment, root_dir, ordering, wid):
    # path, interval and experiment are parameters for apscheduler
    def check_files():
        experiment_management.check_watched_files(path, experiment,
                                                  2, root_dir, ordering, wid)
    # check if folder exists in the path
    if os.path.isdir(path):
        interval = IntervalTrigger(seconds=check_interval)
        print('New watched folder has been added: {0}'.format(path))
        scheduler.add_job(check_files, interval)
    else:
        # notify user that path doesn't exist
        print('Error! The path you mentioned:\n{0}\ndoesn\'t exist!'
              .format(path))
        # if implemented, check for other means of notification


def remove_recurring_task(path):
    scheduler.remove_job(running_scripts[path])
    running_scripts.pop(path)
    return 0


def load_scripts(scripts):
    # scripts = db.get_recurring_scripts()
    [add_recurring_script(s.path, s.recurrence_time) for s in scripts]
    return 0
