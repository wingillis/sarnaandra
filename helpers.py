__author__ = 'wgillis'

import datetime
import ctypes
import os
import platform
import sys

class DiskSpace(object):
    def __init__(self):
        self.spaceAvailable = 0
        self.updated = False

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
            return (free_bytes.value/1024/1024/1024, total.value/1024/1024/1024)
        else:
            st = os.statvfs(path)
            return ((st.f_bavail.value * st.f_frsize.value)/1024/1024/1024, (st.f_blocks.value * st.f_frsize.value)/1024/1024/1024)
    else:
        return mainDisk.spaceAvailable

