import sqlite3
import helpers
import os

__author__ = 'wgillis'

# using sqlite3 to begin with for quick testing, maybe will switch
# to something else in the future like sqlalchemy or psychopg2


class Database(object):
    # class that contains all information about how to interpret the data
    # stored in the database
    def __init__(self):
        self.started = True
        # I did this because it wasn't working for some reason
        self.connection = sqlite3.connect('dataTunes.db',
                                          check_same_thread=False)
        self.closed = False

    def add_experiment(self, experiment_name, data_type):
        c = self.get_cursor()
        date = helpers.get_date()
        c.execute('INSERT INTO experiments VALUES (?,?,?,?,?)',
                  (date, date, data_type, 0, experiment_name))
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

    def add_experiment_file(self, fullfile, experiment, data_type):
        c = self.get_cursor()
        date = helpers.get_date()
        filesize = helpers.get_file_size()
        c.execute('insert into files values (?,?,?,?,?,?,?,?)',
                  (date, date, data_type, filesize,
                   fullfile, experiment, '', ''))

        self.save()
        return 0

    def get_experiment_files(experiment_name):
        ''':params experiment name, string
        :return list of experiment files (formatted in a class)
        '''
        c = self.get_cursor()
        all_files = [f for f in c.execute(
            'select * from files where experiment=?', experiment_name)]
        # convert all_files into a structure
        return all_files

    def add_experiment_files(self):
        '''Given a list of dictionaries with fields the files
                table, this function adds all of them to the database'''
        pass

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
