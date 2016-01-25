from flask import Flask, json, url_for, render_template
import sys
from webbrowser import open_new_tab

app = Flask(__name__, static_folder='static')

@app.route('/')
def main():
    return render_template('index.html')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print('Opening a new tab to server')
        open_new_tab('http://localhost:5000')
    app.run(debug=True)
