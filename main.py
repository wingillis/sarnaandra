from flask import Flask, request, url_for, render_template, redirect, jsonify, send_file
from db_models import *
import helpers
import os
import webbrowser
import threading
import backend
import datetime
import argparse
import platform
import defaults
from subprocess import call as subcall


default_drive_path = os.path.expanduser('~')

# create an instance of the app
app = Flask(__name__)

@app.before_request
def _db_connect():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


@app.route("/")
def main():
    '''the main page, displays all the experiments, total space of the computer
    drive, and where the backup location is'''
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
    '''shows where all the scripts are located'''
    scripts = Scripts.select()
    filt_scripts = list(filter(lambda s: os.path.isfile(s.path), scripts))

    kwargs = {'scripts': filt_scripts, 'main': False, 'reveal_modal': True,
              'script_page': True}
    return render_template('recurring_scripts.html', **kwargs)


@app.route('/add_scripts', methods=['POST', 'get'])
def add_scripts():
    if request.method == 'POST':
        kwargs = {'path': request.form['filepath'],
                  'script_type': request.form['type'],
                  'runtime_interval': request.form['interval'],
                  'tooltip': request.form['tooltip']}
        if os.path.isfile(kwargs['path']):
            fi = os.path.basename(kwargs['path'])
            kwargs['filename'] = fi
            Scripts.create(**kwargs)
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
        path = os.path.expanduser('~')
        t, f = helpers.get_dirs_and_files_in_path(path)
        paths['first'] = True
    else:
        t, f = helpers.get_dirs_and_files_in_path(path)
        fullpath = path
        paths['first'] = False
    paths['files'] = list(f)
    paths['paths'] = list(t)
    paths['fullpath'] = path
    return jsonify(**paths)


@app.route('/exp/<experiment_name>/<page>', methods=['get'])
def see_exp(experiment_name, page=1):
    '''An experiment is selected from the main page and
    the result is given as a variable on this page. This
    page shows the files associated with this experiment'''

    files = Files.select().join(Experiment).where(Experiment.name == experiment_name).order_by(Files.discovered_date.desc()).paginate(int(page), 45)

    # structure the files to be two-pair tuples
    file_struct = helpers.chunks(files.iterator(), 3)

    # kwargs = {'files': files}

    return render_template("experiment_view.html", files=file_struct, page=int(page), expname=experiment_name)


# @app.route('/file/<file_name>', methods=['get'])
# def file_info(file_name):
#     '''Given the path of the file and the filename,
#     this function gives back all the information for
#     that one file'''

#     return 'File information view not implemented yet'


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
    '''Grabs all the variables from form request, and adds them to the
    database'''


    # Three vars from the form
    path = request.form['folderpath']
    strInterval = request.form['timeInterval']
    interval = float(strInterval) if strInterval else defaults.check_folder_interval
    experiment = request.form['expname']

    # check if path exists
    if not os.path.exists(path):
        raise OSError('Path does not exist')
        # the following line may not be needed
        return False

    # we grab this value from the db so that the backend doesn't have
    # access to the db
    root_dir = Settings.get(Settings.key == 'backup_location').value

    # there are 3 keys other than the file extensions
    file_extensions = (len(list(request.form.keys())) - 3)//2
    if file_extensions <= 0:
        print('There are no file extensions, grab everything')
        dtypes = list()
        dtype_vals = list()
    else:
        # construct form key
        dtypes = ['dtype' + str(num) for num in range(file_extensions)]
        extensions = ['extension' + str(num) for num in range(file_extensions)]
        dtype_vals = [request.form[t] for t in dtypes]
        extension_vals = [request.form[t] for t in extensions]

    exp = Experiment.create(date_begin=datetime.datetime.now(),
            date_end=(datetime.datetime.now() + datetime.timedelta(days=365)),
            file_filter=','.join(dtypes), name=experiment,
            ordering='backup_location,experiment,date,file_type',
            scripts_exist=False)
    wfol = WatchedFolder.create(path=path, experiment_id=exp.id,
             check_interval=interval, preserve_folder_structure=False)

    # TODO: add all scripts to each watched folder
    exp_scripts_args = dict(experiment_id=exp.id, save_raw_data=True,
            save_processed_data=False,
            watched_folder_id=wfol.id)
    if file_extensions > 0:
        exp_scripts_args['file_filter'] = dtype_vals[0]
        exp_scripts_args['file_path'] = extension_vals[0]
    ExperimentScripts.create(**exp_scripts_args)
    backend.add_watched_folder(path, interval,
                               experiment, root_dir, exp.ordering.split(','), wfol.id)
    return redirect('/')


@app.route('/delete_folder', methods=['POST'])
def delete_folder():
    folder_id = request.form['id']
    folders = list(WatchedFolder.select().where(WatchedFolder.experiment_id == int(folder_id)))
    WatchedFolder.delete().where(WatchedFolder.experiment_id == int(folder_id))
    for path in folders:
        backend.remove_folder(path.path)
    print('Deleted')
    return redirect('/')


@app.route('/show')
def show():
    filepath = request.args.get('path')
    if platform.system() == 'Windows':
        subcall(['explorer', filepath])
    elif platform.system() == 'Linux':
        subcall(['xdg-open', filepath])
    else:
        subcall(['open', '-R', filepath])
    return redirect(request.referrer)


@app.route('/getpic/<fid>/<index>')
@app.route('/getpic/<fid>/<index>-th')
def send_pic(fid=None, index=None):
    figs = Files.get(Files.id == fid).associated_figures
    fpath = figs.split(',')[int(index)-1]
    _, ext = os.path.splitext(fpath)
    return send_file(fpath, mimetype='image/{0}'.format(ext[1:]))


def start_watching_folders():
    '''On startup, select all watched folders and begin watching them'''
    # get data backup path
    try:
        backend.set_up_folders(WatchedFolder.select(),
                               Settings.get(
                               Settings.key == 'backup_location').value)
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


if __name__ == "__main__":
    # begin watching folders for new files
    # load recurring scripts already programmed into the system
    # the main page loads to a list of the experiments
    parser = argparse.ArgumentParser()
    parser.add_argument('production', nargs='?')
    arguments = parser.parse_args()
    if arguments.production == 'p':
        threading.Timer(1.25,
                        lambda: webbrowser.open('http://127.0.0.1:5000')
                        ).start()
    else:
        app.debug = True
    backend.begin()
    backend.load_scripts(Scripts.select())
    start_watching_folders()

    app.run()
