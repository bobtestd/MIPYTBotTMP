from flask import Flask
from flask import render_template
from flask import request
import configparser
import hashlib
import hmac
from io import BytesIO
import os

secret_file = '/home/bobirdmi/MIPYTBotTMP/config/secret.cfg'
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

    data = request.get_json()
    return ''
    # return data


def verify_signature(secret: str, signature: str, resp_body) -> None:
    """Verify HMAC-SHA1 signature of the given response body.
    The signature is expected to be in format ``sha1=<hex-digest>``.
    """
    try:
        alg, digest = signature.lower().split('=', 1)
    except (ValueError, AttributeError):
        # raise InvalidSignatureError('signature is malformed')
        raise 'Error: signature is malformed'

    if alg != 'sha1':
        # raise InvalidSignatureError("expected type sha1, but got %s" % alg)
        raise("Error: expected type sha1, but got %s" % alg)

    computed_digest = hmac.new(secret.encode('utf-8'),
                               msg=resp_body,
                               digestmod=hashlib.sha1).hexdigest()

    if not hmac.compare_digest(computed_digest, digest):
        # raise InvalidSignatureError('digests do not match')
        raise 'Error: digests do not match'


def run_local_web():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)


# class InvalidSignatureError(HTTPError):
#     def __init__(self, message: str, **kwargs) -> None:
#         msg = "Invalid X-Hub-Signature: %s" % message
#         super().__init__(status=403, body=msg, **kwargs)

if __name__ == '__main__':
    run_local_web()