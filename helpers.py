import datetime
import ctypes
import os
import platform
import sys
import toolz
from db_models import Files

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
        # returns space available and total space
        return (self.spaceAvailable, self.totalSpace)


mainDisk = DiskSpace()


def get_File_Class():
    return Files


def get_date():
    return datetime.date.today().isoformat()


def generate_default_backup(path):
    return os.path.join(path, 'sarnaandra', 'backup')


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


def chunks(iterable, n):
    l = list(iterable)
    for i in range(0, len(l), n):
        yield tuple(l[i:i+n])


def get_dirs_and_files_in_path(path):
    # filter function
    def isdir(a): return os.path.isdir(a)
    # gives the opposite results as above
    not_isdir = toolz.complement(isdir)

    if not path and platform.system() == 'Windows':
        import win32api
        drives = win32api.GetLogicalDriveStrings()
        drives = [d for d in drives.split('\000') if d]
        return drives

    elif os.path.exists(path):
        r = os.listdir(path)
        # 2x acccess means I have to remove the generator
        f = [os.path.join(path, a) for a in r]
        dirs = filter(isdir, f)
        files = filter(not_isdir, f)

    else:
        try:
            head, tail = os.path.split(path)
            r = os.listdir(head)
            filtered_everything = filter(lambda a: a.startswith(tail), r)
            # because this was accesssed twice, I needed to remove the generator
            filtered_everything = [os.path.join(head, a) for a in filtered_everything]
            dirs = filter(isdir, filtered_everything)
            files = filter(not_isdir, filtered_everything)

        except Exception as e:
            print('{0} doesn\'t even exist you stupid'.format(head))
            return None

    result = (sorted(list(toolz.take(100, dirs))),
              sorted(list(toolz.take(100, files))))
    return result
