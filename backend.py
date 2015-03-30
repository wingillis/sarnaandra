__author__ = 'wgillis'

import importlib
import threading

def add_recurring_task(path, recurrence_time):
    '''adds a file (currently only python scripts)
        to be run once every recurrence_time (which is in seconds'''
    library = importlib.import_module(path)
