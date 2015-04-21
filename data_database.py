import sqlite3
import helpers
import os

__author__ = 'wgillis'

# using sqlite3 to begin with for quick testing, maybe will switch
# to something else in the future like sqlalchemy or psychopg2 or mongodb


class Database(object):
    # class that contains all information about how to interpret the data
    # stored in the database
    def __init__(self):
        self.started = True
        # I did this because threading wasn't working for some reason
        self.connection = sqlite3.connect('dataTunes.db',
                                          check_same_thread=False)
        self.closed = False

    def add_experiment(self, expname, dtype, folderpath, timeInterval):
        c = self.get_cursor()
        date = helpers.get_date()
        # values are: (date_begin, date_end, data_type,
        # files(number), experiment name, folder path)
        c.execute('INSERT INTO experiments VALUES (?,?,?,?,?,?,?)',
                  (date, date, dtype, 0, expname, folderpath, timeInterval))
        self.save()
        return 0

    def get_all_experiments(self):
        '''Tuple of (start date, modified date,
            data type, # files, experiment name)'''
        c = self.get_cursor()
        vals = [exp for exp in c.execute('select * from experiments')]
        return vals

    def save(self):
        self.connection.commit()

    def get_cursor(self):
        return self.connection.cursor()

    def close(self):
        self.connection.close()
        self.closed = True
        return 0

    def get_tables(self):
        '''Returns a list of tables implemented in this database'''
        c = self.get_cursor()
        return list(map(lambda a: a[0], c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()))

    def add_experiment_file(self, fullfile, experiment, data_type):
        c = self.get_cursor()
        date = helpers.get_date()
        filesize = helpers.get_file_size()
        c.execute('insert into files values (?,?,?,?,?,?,?,?)',
                  (date, date, data_type, filesize,
                   fullfile, experiment, '', ''))

        self.save()
        return 0

    def get_watched_folders(self):
        c = self.get_cursor()
        watched_folders = [s for s in c.execute('select path, experiment, data_type from watched_folders')]
        interval = float(self.get_setting('watch_folder_interval'))
        watched_folders = map(lambda a: (a[0], interval, a[1], a[2]), watched_folders)
        if type(watched_folders) is list:
            return watched_folders
        else:
            return list(watched_folders)

    def get_experiment_files(experiment_name):
        ''':params experiment name, string
        :return list of experiment files (formatted in a class)
        '''
        c = self.get_cursor()
        all_files = [f for f in c.execute(
            'select * from files where experiment=?', experiment_name)]
        # convert all_files into a structure (currently done in main script)
        return all_files

    def add_experiment_files(self):
        '''Given a list of dictionaries with fields the files
                table, this function adds all of them to the database'''
        pass

    def get_experiment_ordering(self, experiment):
        '''Just a testing implementation. Returns the same ordering
        every time'''
        return ['backup_location', 'experiment', 'date', 'file_type']

    def add_recurring_script(self, fullfile, type, interval):
        '''Adds an entry for a recurring script.
        Interval is in hours.'''
        c = self.get_cursor()
        c.execute('''insert into recurring_files (filename, script_type,
             time_interval) values (?,?,?)''', (fullfile, type, interval))
        self.save()
        return 0

    def get_recurring_scripts(self):
        '''gets a list of all scripts that will run repeatedly
        '''
        c = self.get_cursor()
        scripts = [s for s in c.execute('''select filename,
            script_type, time_interval from recurring_files''')]
        return scripts

    def add_table(self, exec_string):
        '''Only used very rarely, in setup in the beginning. Creates tables
        needed by the program to run'''
        c = self.get_cursor()
        c.execute(exec_string)
        return 0

    def create_settings(self):
        c = self.get_cursor()
        c.execute('insert into settings (k, v) values (?,?)',
                  ('backup_location', ''))
        c.execute('insert into settings (k, v) values (?,?)',
                  ('backup_name', ''))
        c.execute('insert into settings (k,v) values (?,?)',
                  ('watch_folder_interval', '10'))
        self.save()

    def get_all_settings(self):
        c = self.get_cursor()
        sett = [s for s in c.execute('select * from settings')]
        return sett

    def update_settings(self, k, v):
        c = self.get_cursor()
        c.execute('update settings set v=? where k=?', (v, k))
        self.save()

    def get_setting(self, k):
        c = self.get_cursor()
        return c.execute('select v from settings where k=?',
                         (k,)).fetchone()[0]

    def get_watched_folder(self):
        c = self.get_cursor()

    def add_watched_folder(self):
        return 'I AM A WATCHED FOLDER'
