

def run(db_handle, list_of_tables):
	'''Runs all the necessary functions to make any databases not in the 
	database yet.'''
	table_execute = {'experiments': '',
					 'files': '',
					 'recurring_files': '',
					 'watched_folders': '',
					 'settings': ''}
	tables = db_handle.get_tables()
	c = db_handle.get_cursor()
	current_tables = map(lambda a: a[0], c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
	for key in table_execute.keys():
		if key not in current_tables:
			c.execute(table_execute[key])

	c.commit()

