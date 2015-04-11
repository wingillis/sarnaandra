

def run(db_handle):
    '''Runs all the necessary functions to make any databases not in the
    database yet.'''
    table_execute = {'experiments': 'CREATE TABLE experiments(date_begin text, date_end text, data_type text, files text, name text, folder_paths text)',
                     'files': 'CREATE TABLE files(date_added text, date_modified text, data_type text, filesize real, name text, experiment text, tags text, additional_files text)',
                     'recurring_files': 'CREATE TABLE recurring_files(id Primary key int, filename text, script_type text, time_interval real)',
                     'watched_folders': "CREATE TABLE watched_folders(id int primary key, path text, experiment text, data_type text)",
                     'settings': 'CREATE TABLE settings'}
    tables = db_handle.get_tables()
    for key in table_execute.keys():
        if key not in tables:
            db_handle.add_table(table_execute[key])

    db_handle.save()
