from flask import Flask, request, url_for, render_template, redirect, jsonify
from db_models import *
import helpers
import os
import webbrowser
import threading
import backend
import make_database
import datetime
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('production', nargs='?')
arguments = parser.parse_args()

default_drive_path = os.path.expanduser('~')

if arguments.production is 'production':
    production = True
else:
    production = False

# create an instance of the app
app = Flask(__name__)

# make_database.run(base)

backend.begin()


@app.before_request
def _db_connect():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


# begin watching folders for new files
try:
    backend.set_up_folders(WatchedFolder.select(),
                           Settings.get(Settings.key == 'backup_location').value)
except DoesNotExist as e:
    print('No settings yet')
    _db_connect()
    tempp = helpers.generate_default_backup(default_drive_path)
    Settings.create(key='backup_location',
                    value=tempp)
    if not os.path.exists(tempp):
        os.makedirs(tempp)
    print('Generated default backup location')
    _db_close(' ')
# load recurring scripts already programmed into the system
backend.load_scripts(Scripts.select())
# the main page loads to a list of the experiments


@app.route("/")
def main():
    exps = Experiment.select()
    backup = Settings.get(Settings.key == 'backup_location').value
    (space, total) = helpers.get_free_disk_space(backup)
    kwargs = {'experiments': exps, 'freespace': round(space, 2),
              'totalspace': round(total, 2),
              'percentage': round(float(space)/total*100, 2),
              'drive': backup,
              'main': True,
              'reveal_modal': True,
              'backup': backup}
    return render_template('exp_lists.html', **kwargs)


@app.route('/recurring_scripts', methods=['get'])
def recurring_scripts():
    scripts = Scripts.select()
    filt_scripts = list(filter(lambda s: os.path.isfile(s.path), scripts))

    kwargs = {'scripts': filt_scripts, 'main': False, 'reveal_modal': True}
    return render_template('recurring_scripts.html', **kwargs)


@app.route('/add_scripts', methods=['POST', 'get'])
def add_scripts():
    if request.method == 'POST':
        kwargs = {'path': request.form['filepath'],
                  'script_type': request.form['type'],
                  'runtime_interval': request.form['interval'],
                  'tooltip': request.form['tooltip']}
        if helpers.file_exists(kwargs['path']):
            p, fi = os.path.splitext(kwargs['path'])
            kwargs['filename'] = fi
            Scripts.create(**kwargs)
            # base.add_recurring_script(**kwargs)  # to database
            backend.add_recurring_script(kwargs['path'],
                                         kwargs['runtime_interval'])
        else:
            # alert user that file doesn't exist
            print('File does not exist')
    return redirect('/recurring_scripts')


@app.route('/filepath')
def get_next_dirs():
    # assumes path is located in
    path = request.args.get('path')
    paths = {}
    if path == '__base__':
        fullpath = os.path.expanduser('~')
        dir_list = helpers.get_dirs_in_path(fullpath)
        paths['first'] = True
    else:
        dir_list = helpers.get_dirs_in_path(path)
        fullpath = path
        paths['first'] = False
    paths['files'] = helpers.get_files_in_path(fullpath)
    paths['paths'] = dir_list
    paths['fullpath'] = fullpath
    return jsonify(**paths)


@app.route('/exp/<experiment_name>', methods=['get'])
def see_exp(experiment_name):
    '''An experiment is selected from the main page and
    the result is given as a variable on this page. This
    page shows the files associated with this experiment'''

    files = base.get_experiment_files(experiment_name)
    formatted_files = helpers.format_files(files)
    kwargs = {'files': formatted_files}

    return 'Experiment name: {0}'.format(experiment_name)


@app.route('/file/<file_name>', methods=['get'])
def file_info(file_name):
    '''Given the path of the file and the filename,
    this function gives back all the information for
    that one file'''

    return 'File information view not implemented yet'


@app.route('/settings', methods=['get', 'post'])
def settings():
    '''Displays the settings for the current user'''
    settings = Settings.select()
    return render_template('settings.html', setting=settings)


@app.route('/change_setting/<s_name>', methods=['post'])
def change_setting(s_name=None):
    '''Quick implementation of settings change. May be able to be
    implemented differently. Updates setting variable in database'''
    if s_name:
        s = Settings.get(Settings.key == s_name)
        s.value = request.form[s_name]
        s.save()
    return redirect('/settings')


@app.route('/add_watched_folder', methods=['get', 'POST'])
def main_add_watched_folder():
    path = request.form['folderpath']
    interval = float(request.form['timeInterval'])
    experiment = request.form['expname']
    root_dir = Settings.get(Settings.key == 'backup_location').value
    # there are 3 keys
    file_extensions = (len(list(request.form.keys())) - 3)/2

    dtypes = ['dtype' + str(num) for num in range(file_extensions)]
    extensions = ['extension' + str(num) for num in range(file_extensions)]
    dtype_vals = [request.form[t] for t in dtypes]
    extension_vals = [request.form[t] for t in extensions]
    exp = Experiment.create(date_begin=datetime.datetime.now(), date_end=(datetime.datetime.now()+ datetime.timedelta(days=365)), file_filter=','.join(dtypes), name=experiment, ordering='backup_location,experiment,date,file_type')
    print(exp)
    print(exp.id)
    print(exp.name)
    WatchedFolder.create(path=path, experiment_id=exp.id, check_interval=interval)
    # base.add_experiment(experiment, ','.join(dtype_vals), path, interval)
    backend.add_watched_folder(path, interval,
                               experiment, root_dir, exp.ordering.split(','))
    return redirect('/')


def start_watching_folders():

    # get data backup path
    root_dir = Settings.get(Settings.key == 'backup_location')
    backend.set_up_folders(WatchedFolder.select(), root_dir)


if __name__ == "__main__":

    if production:
        threading.Timer(1.25,
                        lambda: webbrowser.open('http://127.0.0.1:5000')
                        ).start()
    else:
        app.debug = True
    start_watching_folders()

    app.run()
