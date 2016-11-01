import githubissuesbot
import pytest
import betamax
import os
import configparser


auth_file = 'tests/fixtures/auth.cfg.test'
auth_betamax_file = 'tests/fixtures/auth.cfg.truetoken.test'
label_file = 'tests/fixtures/label.cfg.test'
test_url = 'https://api.github.com/repos/bobtestd/MIPYTBotTMP/issues'

with betamax.Betamax.configure() as config:
    # tell Betamax where to find the cassettes
    # make sure to create the directory
    config.cassette_library_dir = 'tests/fixtures/cassettes'

    if os.path.isfile(auth_betamax_file):
        # If the tests are invoked with an auth_betamax_file exists
        conf = configparser.ConfigParser()
        conf.read(auth_betamax_file)
        TOKEN = conf['github']['token']
        # Always re-record the cassetes
        # https://betamax.readthedocs.io/en/latest/record_modes.html
        config.default_cassette_options['record_mode'] = 'all'
    else:
        TOKEN = 'false_token'
        # Do not attempt to record sessions with bad fake token
        config.default_cassette_options['record_mode'] = 'none'

    # Hide the token in the cassettes
    config.define_cassette_placeholder('<TOKEN>', TOKEN)


@pytest.fixture
def githubbot():
    return githubissuesbot.GitHubBot(auth_file, label_file, test_url, 'default')


@pytest.fixture
def githubbot_betamax(betamax_session):
    return githubissuesbot.GitHubBot('', label_file, test_url, 'default', session=betamax_session, auth_token=TOKEN)


@pytest.mark.parametrize('label', ('bug', 'duplicate', 'enhancement', 'help wanted', 'invalid', 'question', 'wontfix'))
def test_read_config_labels(githubbot, label):
    assert label in githubbot._label_list


@pytest.mark.parametrize('label_rule', ('bug|problem', 'same', 'enhance', 'help|advise', 'invalid', 'ask', 'fix'))
def test_read_config_label_rules(githubbot, label_rule):
    assert label_rule in githubbot._label_rules


def test_read_config_auth(githubbot):
    assert githubbot._token == 'authok'


def test_label_all_issues(githubbot_betamax):
    issue_nums = range(15, 21)
    results = githubbot_betamax.label_all_issues(True)

    # verify response codes
    for i in issue_nums:
        assert results[i][1] == 200

    # verify label results
    assert set(results[15][0]) == {'bug'}
    assert set(results[16][0]) == {'help wanted'}
    assert set(results[17][0]) == {'wontfix'}
    assert set(results[18][0]) == {'default'}
    assert set(results[19][0]) == {'bug', 'duplicate', 'help wanted'}
    assert set(results[20][0]) == {'invalid', 'enhancement'}
