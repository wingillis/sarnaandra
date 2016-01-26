from flask import json, url_for, render_template
import sys
from app import app
from webbrowser import open_new_tab
from api import api
from models import *

app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def main():
    return app.send_static_file('index.html')

@app.route('/exp/<name>')
def experiment_page(name=None):
    exp = Experiment.select().where(Experiment.id==name)
    return 'Nothing'

if __name__ == "__main__":
    create_tables()
    if len(sys.argv) > 1:
        print('Opening a new tab to server')
        open_new_tab('http://localhost:5000')
    app.run(debug=True)
