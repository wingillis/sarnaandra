import datetime
import ctypes
import os
import platform
import sys
import toolz

__author__ = 'wgillis'


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


class FileProperties(object):
    '''Attributes of each file for use in the
    experiment files view'''
    def __init__(self, **kwargs):
        self.date_added = kwargs['date_added']
        self.date_modified = kwargs['date_modified']
        self.data_type = kwargs['data_type']
        self.filesize = kwargs['filesize']
        self.name = kwargs['name']
        self.experiment = kwargs['experiment']
        self.tags = kwargs['tags']
        self.additional_files = kwargs['additional_files']


mainDisk = DiskSpace()


def get_date():
    return datetime.date.today().isoformat()


# returns amount of free disk space of the path
def get_free_disk_space(path):
    if not mainDisk.updated:
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            total = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(path),
                                                       None,
                                                       ctypes.pointer(total),
                                                       ctypes.pointer(
                                                       free_bytes))
            mainDisk.update_space(free_bytes.value/1024/1024/1024,
                                  total.value/1024/1024/1024)
            return mainDisk.get_space()
        else:
            st = os.statvfs(path)
            mainDisk.update_space((st.f_bavail * st.f_frsize)/1024.0/1024/1024,
                                  (st.f_blocks * st.f_frsize)/1024.0/1024/1024)
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

    return [ScriptProperties(*s, tooltip=tip[i]) for i, s in enumerate(script_list)]


def format_files(file_list):
    ''':params list of files
    :return FileProperties object list
    These files are now formatted to use with jinja
    '''
    kwarg_file_list = map(make_file_kwargs, file_list)
    f_files = list(map(lambda a: FileProperties(**a), kwarg_file_list))
    return f_files


def get_ordering(experiment, db):
    ordering = db.get_experiment_ordering(experiment)
    return ordering


def get_settings(db):
    settings = db.get_all_settings()
    return settings


def make_file_kwargs(file_list):
    ''':params List of files (in tuple format)
    '''
    return_list = []
    kwargs = {}
    for file in file_list:
        kwargs['date_added'] = file[0]
        kwargs['date_modified'] = file[1]
        kwargs['data_type'] = file[2]
        kwargs['filesize'] = file[3]
        kwargs['name'] = file[4]
        kwargs['experiment'] = file[5]
        kwargs['tags'] = file[6]
        kwargs['additional_files'] = file[7]
        return_list.append(kwargs)

    return return_list


def file_exists(path):
    return os.path.isfile(path)


def get_dirs_in_path(path):
    if not path and platform.system() == 'Windows':
        import win32api
        drives = win32api.GetLogicalDriveStrings()
        drives = [d for d in drives.split('\000') if d]
        return drives
    try:
        fs = os.listdir(path)
        directories = [s for s in fs if os.path.isdir(os.path.join(path, s))]
    except Exception as e:
        print('Exception occurred')
        print(e)
        try:
            head, tail = os.path.split(path)
            fs = os.listdir(head)
            directories = filter(lambda a: a.lower().startswith(tail.lower()), fs)
            directories = list(filter(lambda a:
                               os.path.isdir(os.path.join(head, a)), directories))
        except:
            return None
    return directories


def get_files_in_path(path):
    if path:
        try:
            fs = os.listdir(path)
            directories = [s for s in fs if not os.path.isdir(os.path.join(path, s))]
        except Exception as e:
            print('Exception occurred')
            print(e)
            try:
                head, tail = os.path.split(path)
                fs = os.listdir(head)
                directories = filter(lambda a: a.lower().startswith(tail.lower()), fs)
                directories = filter(lambda a:
                                     not os.path.isdir(os.path.join(head, a)), directories)
            except:
                return None
        return list(toolz.take(100, directories))