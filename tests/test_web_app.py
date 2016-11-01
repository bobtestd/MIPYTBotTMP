import pytest
import markdown
from githubissuesbot.web_app import app
from githubissuesbot import web_app


fake_secret = '3ce92e588556bdh7220bc738b4dafad15bj7c196'
body = 'this is my signature!'.encode('utf-8')


@pytest.fixture
def testapp():
    app.config['TESTING'] = True
    return app.test_client()


def test_main_page(testapp):
    with open('README.md', 'r') as f:
        assert markdown.markdown(f.read()) in testapp.get('/').data.decode('utf-8')


def test_verify_good_signature():
    good_signature = 'sha1=18fdf73c44d3a4b72b55b382c494f35a25b3a6e5'

    web_app.verify_signature(fake_secret, good_signature, body)


def test_verify_bad_signature():
    bad_signature = 'sha1=18fdf73c44d3a4c72b55b382c494f35a25b3a6e5'

    with pytest.raises(Exception):
        web_app.verify_signature(fake_secret, bad_signature, body)


