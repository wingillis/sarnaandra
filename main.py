from flask import Flask, request, url_for, render_template,redirect
import data_database as db
import platform
import helpers
import os
import webbrowser
import threading
import backend

if platform.system() == 'Windows':
    default_drive_path = 'C:\\'
else:
    default_drive_path = os.path.expanduser('~')

production = True

# create an instance of the app
app = Flask(__name__)

# open the database
base = db.Database()

# the main page loads to a list of the experiments
@app.route("/")
def main():
    exps = base.get_all_experiments()
    (space, total) = helpers.get_free_disk_space(default_drive_path)
    kwargs = {'experiments': exps, 'freespace': round(space, 2), 'totalspace': round(total, 2),
              'percentage': round(float(space)/total*100,2), 'drive': default_drive_path,
              'main': True}
    return render_template('exp_lists.html', **kwargs)

@app.route("/add_experiment", methods=['post', 'get'])
def add_exp():
    if request.method == 'POST':
        base.add_experiment(request.form['expname'], request.form['dtype'])
    return redirect('/')

@app.route('/recurring_scripts', methods=['post', 'get'])
def recurring_scripts():
    if request.method == 'POST':
        kwargs = {'fullfile': request.form['filepath'],
                  'type': request.form['type'],
                  'interval': request.form['interval']}
        if helpers.file_exists(kwargs['fullfile']):
            base.add_recurring_script(**kwargs)

        else:
            # alert user that file doesn't exist
            pass
    elif request.method == 'GET':
        scripts = base.get_recurring_scripts()
        if scripts:
            scripts = helpers.format_scripts(scripts)
            kwargs = {'scripts': scripts, 'main': False}
            return render_template('recurring_scripts.html', **kwargs)
        else:
            kwargs = {'scripts':None, 'main': False}
            return render_template('recurring_scripts.html', **kwargs)


if __name__=="__main__":

    if production:
        threading.Timer(1.25, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    else:
        app.debug = True

    app.run()