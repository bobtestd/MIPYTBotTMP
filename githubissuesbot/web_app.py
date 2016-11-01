from flask import Flask
from flask import render_template
from flask import request
import configparser
import hashlib
import hmac
import markdown
import appdirs
from socket import gethostname
import pkg_resources


def _read_web_config():
    global conf
    conf.read(web_config_file)

    global secret_file
    secret_file = conf['github']['secret_file']

    global auth_file
    auth_file = conf['github']['auth_file']

    global label_file
    label_file = conf['github']['label_file']

    # read file with a secret token for webhook
    conf.read(secret_file)


app_name = __name__.split('.')[0]
app = Flask(app_name)
conf = configparser.ConfigParser()

# if it is running on pythonanywhere.com (maybe that code works for other hosts)
if 'liveweb' in gethostname():
    import github_bot
    # set "web_config_file" variable to file with web configuration
    # format: /home/<username>/<project_name>/path/to/webcfg.cfg
    web_config_file = '/home/bobirdmi/MIPYTBotTMP/githubissuesbot/config/web.cfg'
    # read web configurations
    _read_web_config()
else:
    from . import github_bot


@app.route('/')
def index():
    readme_text = pkg_resources.resource_stream(app_name, 'README.md')

    return render_template('index.html', readme_text=readme_text.read().decode("utf-8"))


@app.route('/hook', methods=['POST'])
def hook():
    verify_signature(conf['github']['secret_token'],
                     request.headers['X-Hub-Signature'],
                     request.data)

    req_json = request.get_json()
    if req_json['action'] == 'opened':
        bot = github_bot.GitHubBot(auth_file, label_file, None, 'default')
        bot.label_issue(req_json['issue'])

    return str(req_json['issue']['url']) + ', ' + str(req_json['issue']['title']) + ', ' \
           + str(req_json['issue']['body']) + ', ' + str(req_json['issue']['labels']) + ', ' \
           + str(req_json['action'])


@app.template_filter('markdown')
def convert_markdown(text):
    """Convert markdown text to html"""
    return markdown.markdown(text)


def verify_signature(secret: str, signature: str, resp_body) -> None:
    """Verify HMAC-SHA1 signature of the given response body.
    The signature is expected to be in format ``sha1=<hex-digest>``.
    """
    try:
        alg, digest = signature.lower().split('=', 1)
    except (ValueError, AttributeError):
        raise Exception('Error: signature is malformed')

    if alg != 'sha1':
        raise Exception("Error: expected type sha1, but got %s" % alg)

    computed_digest = hmac.new(secret.encode('utf-8'),
                               msg=resp_body,
                               digestmod=hashlib.sha1).hexdigest()

    if not hmac.compare_digest(computed_digest, digest):
        raise Exception('Error: digests do not match')


def run_local_web(web_config):
    global web_config_file
    if web_config:
        web_config_file = web_config
    else:
        web_config_file = appdirs.site_config_dir(appname=app_name) + '/web.cfg'

    # read web configuration
    _read_web_config()

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
