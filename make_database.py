

def run(db_handle, list_of_tables):
    '''Runs all the necessary functions to make any databases not in the
    database yet.'''
    table_execute = {'experiments': '',
                     'files': '',
                     'recurring_files': '',
                     'watched_folders': '',
                     'settings': ''}
    tables = db_handle.get_tables()
    for key in table_execute.keys():
        if key not in tables:
    		db_handle.add_table(table_execute[key])

    db_handle.save()

