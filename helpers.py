__author__ = 'wgillis'

import datetime
import ctypes
import os
import platform
import sys

class DiskSpace(object):
    def __init__(self):
        self.spaceAvailable = 0
        self.totalSpace = 0
        self.updated = False

    def update_space(self, free_space, totalSpace):
        self.spaceAvailable = free_space
        self.totalSpace = totalSpace
        self.updated = True

    def get_space(self):
        return (self.spaceAvailable, self.totalSpace)

class ScriptProperties(object):
    '''Attributes of each script formatted for the
    UI'''
    def __init__(self, filename, script_type, time_interval, tooltip):
        self.name = filename
        self.type = script_type
        self.interval = time_interval
        self.tooltip = tooltip

mainDisk = DiskSpace()


def get_date():
    return datetime.date.today().isoformat()


def get_free_disk_space(path):
    if not mainDisk.updated:
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            total = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(path),
                None, ctypes.pointer(total), ctypes.pointer(free_bytes))
            mainDisk.update_space(free_bytes.value/1024/1024/1024, total.value/1024/1024/1024)
            return mainDisk.get_space()
        else:
            st = os.statvfs(path)
            mainDisk.update_space((st.f_bavail * st.f_frsize)/1024.0/1024/1024, (st.f_blocks * st.f_frsize)/1024.0/1024/1024)
            return mainDisk.get_space()
    else:
        return mainDisk.get_space()


def hour2seconds(hour):
    '''converts the given hour variable to seconds'''
    seconds = float(hour) * 60 * 60
    return seconds


def format_scripts(script_list, tip):
    '''given a list of script tuples from the database,
    this adds each scipt to a structure to be properly shown in
        the web browser'''

    return [ScriptProperties(*s, tooltip=tip[i]) for i,s in enumerate(script_list)]

def file_exists(path):
    return os.path.isfile(path)

def get_dirs_in_path(path):
    fs = os.listdir(path)
    directories = [s for s in fs if os.path.isdir(os.path.join(path, s))]
    return directories