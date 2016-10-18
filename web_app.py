from flask import Flask
from flask import render_template
from flask import request
import configparser
import hashlib
import hmac
import os
import github_bot

config_path = '/home/bobirdmi/MIPYTBotTMP/config/'
secret_file = config_path + 'secret.cfg'
auth_file = config_path + 'auth.cfg'
label_file = config_path + 'label.cfg'
app = Flask(__name__)


@app.route('/')
def index(some_name='fsdfdsf'):
    return render_template('index.html', name=some_name)


@app.route('/hook', methods=['POST'])
def hook():
    conf = configparser.ConfigParser()
    conf.read(secret_file)
    verify_signature(conf['github']['secret_token'],
                    #os.environ['SECRET_TOKEN'],
                     request.headers['X-Hub-Signature'],
                     request.data)

    # data = request.get_json()

    bot = github_bot.GitHubBot(auth_file, label_file, None, 'default')
    bot.label_issue(request.get_json()['issue'])

    return [request.get_json()['issue']['url'], request.get_json()['issue']['title'],
            request.get_json()['issue']['body'], request.get_json()['issue']['labels']]


def verify_signature(secret: str, signature: str, resp_body) -> None:
    """Verify HMAC-SHA1 signature of the given response body.
    The signature is expected to be in format ``sha1=<hex-digest>``.
    """
    try:
        alg, digest = signature.lower().split('=', 1)
    except (ValueError, AttributeError):
        raise 'Error: signature is malformed'

    if alg != 'sha1':
        raise("Error: expected type sha1, but got %s" % alg)

    computed_digest = hmac.new(secret.encode('utf-8'),
                               msg=resp_body,
                               digestmod=hashlib.sha1).hexdigest()

    if not hmac.compare_digest(computed_digest, digest):
        raise 'Error: digests do not match'


def run_local_web():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
