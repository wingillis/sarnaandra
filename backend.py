import importlib
import os
import sys
import helpers
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

__author__ = 'wgillis'


scheduler = None


def begin():
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()


running_scripts = {}
tool_tips = {}


def print_jobs():
    print('Printing get jobs')
    f = scheduler.get_jobs()
    for i in f:
        print(i)


def add_recurring_task(p, recurrence_time):
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
    [add_recurring_task(s[0], s[2]) for s in scripts]
    return 0
