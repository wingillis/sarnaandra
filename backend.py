import importlib
import os
import sys
import helpers
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

__author__ = 'wgillis'


scheduler = None

running_scripts = {}
tool_tips = {}

def begin():
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()


def set_up_folders(db):
    # each index of watched_folders contains a tuple of the 
    # folder location, recurrence time and experiment
    watched_folders = db.get_watched_folders()
    for (folder_location, recurrence_time, experiment) in watched_folders:
        add_watched_folder(folder_location, recurrence_time, experiment)


def print_jobs():
    print('Printing get jobs')
    f = scheduler.get_jobs()
    for i in f:
        print(i)


def add_recurring_script(p, recurrence_time):
    '''adds a file (currently only python scripts)
        to be run once every recurrence_time (which is in seconds)'''
    if helpers.file_exists(p):
        scheduler.print_jobs()
        path, file = os.path.split(p)
        sys.path.append(path)
        library = importlib.import_module(file[:-3])
        tool_tips[p] = library.run.__doc__
        print('Importing module {1} from {0}'.format(path, file))
        interval = IntervalTrigger(seconds=int(recurrence_time))
        if p not in running_scripts:
            running_scripts[p] = scheduler.add_job(library.run, interval)
        scheduler.print_jobs()
        return 0
    else:
        return 1


def add_watched_folder(path, check_interval, experiment):
    # path, interval and experiment are parameters for apscheduler
    pass


def remove_recurring_task(path):
    scheduler.remove_job(running_scripts[path])
    running_scripts.pop(path)
    return 0


def get_tool_tips(path):
    # do better managing of tool tip presence
    if tool_tips[path]:
        return tool_tips[path]
    else:
        return None


def load_scripts(db):
    scripts = db.get_recurring_scripts()
    [add_recurring_script(s[0], s[2]) for s in scripts]
    return 0
