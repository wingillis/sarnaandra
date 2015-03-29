__author__ = 'wgillis'

# using sqlite3 to begin with for quick testing, maybe will switch
# to something else in the future like sqlalchemy or psychopg2
import sqlite3
import helpers

class Database(object):
    # class that contains all information about how to interpret the data
    # stored in the database
    def __init__(self):
        self.started = True
        self.connection = sqlite3.connect('dataTunes.db', check_same_thread=False)

    def add_experiment(self, experiment_name, data_type):
        c = self.get_cursor()
        date = helpers.get_date()
        c.execute('INSERT INTO experiments VALUES (?,?,?,?,?)', (date, date, data_type, 0, experiment_name))
        self.save()
        return 0

    def get_all_experiments(self):
        c = self.get_cursor()
        vals = [exp for exp in c.execute('select * from experiments')]
        return vals

    def save(self):
        self.connection.commit()

    def get_cursor(self):
        return self.connection.cursor()

    def close(self):
        self.connection.close()
        return 0
