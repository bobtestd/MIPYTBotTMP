from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def index(some_name='fsdfdsf'):
    return render_template('index.html', name=some_name)


@app.route('/hook', methods=['POST'])
def hook():
    data = request.get_json()
    # return ''
    return data


def run_web():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)