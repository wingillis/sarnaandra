__author__ = 'wgillis'

import importlib
import os
import sys

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = BackgroundScheduler()
scheduler.start()

running_scripts = {}

def add_recurring_task(path, file, recurrence_time):
    '''adds a file (currently only python scripts)
        to be run once every recurrence_time (which is in seconds)'''
    sys.path.append(path)
    library = importlib.import_module(file[:-3])
    print('Importing module {1} from {0}'.format(path, file))
    interval = IntervalTrigger(seconds=int(recurrence_time))
    running_scripts[path] = scheduler.add_job(library.run, interval)
    return 0


def remove_recurring_task(path):
    scheduler.remove_job(running_scripts[path])
    running_scripts.pop(path)
    return 0