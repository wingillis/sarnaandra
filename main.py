from flask import Flask, request, url_for, render_template,redirect
import data_database as db
import platform
import helpers
import os

if platform.system() == 'Windows':
    default_drive_path = 'C:\\'
else:
    default_drive_path = os.path.expanduser('~')

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
              'percentage': round(float(space)/total*100,2), 'drive': default_drive_path}
    return render_template('exp_lists.html', **kwargs)

@app.route("/add_experiment", methods=['post', 'get'])
def add_exp():
    if request.method == 'POST':
        base.add_experiment(request.form['expname'], request.form['dtype'])
    return redirect('/')

if __name__=="__main__":
    app.debug = True
    app.run()