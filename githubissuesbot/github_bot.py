import requests
import json
import configparser
import re
import logging


logging.basicConfig(filename='github_bot.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


class GitHubBot:
    def __init__(self, auth_file, label_file, url, default_label, session=None, auth_token=None):
        """
        A constructor.

        :param auth_file: path to file with authorization info. If you don't want to read file, you may use auth_token.
        :param label_file: path to file with issue labels and their rules.
        :param url: Url of issues in repo (ex.: https://api.github.com/repos/<username>/<repo>/issues).
        If you want to label ALL issues in this repo, you MUST specify this parameter. Otherwise,
        set it to None in case of labeling only one issue.
        :param default_label: If no rule can be applied to issue, an issue will be labeled by this string.
        :param session: Session for handling network communication. If it is None, requests.Session() will be invoked.
        :param auth_token: GitHub Personal Access Token. If it is None, the auth_file will be read. Otherwise, the
        value of this variable will be used for authorization and auth_file parameter will be ignored.
        """
        self._read_config(auth_file, auth_token, label_file)

        self.url = url
        self.default_label = default_label

        self._session = session or requests.Session()
        self._session.headers = {'Authorization': 'token ' + self._token, 'User-Agent': 'Python'}

    def _read_config(self, auth_file, auth_token, label_file):
        conf = configparser.ConfigParser()

        if auth_token:
            conf.read(label_file)
            self._token = auth_token
        else:
            conf.read([auth_file, label_file])
            self._token = conf['github']['token']

        self._label_list = list(map(str.strip, conf['list']['labels'].split(',')))
        logging.debug("List of defined labels:", self._label_list)

        self._label_rules = []
        for label in self._label_list:
            self._label_rules.append(conf['rules'][label])

    def label_all_issues(self, label_comments):
        r = self._session.get(self.url)
        r.raise_for_status()

        results = {}

        for issue_info in r.json():
            if issue_info['labels']:
                continue

            results[issue_info['number']] = self._set_labels(self.url + '/' + str(issue_info['number']),
                                                             issue_info['title'],
                                                             issue_info['body'],
                                                             label_comments)

        return results

    def label_issue(self, issue_info):
        if not issue_info['labels']:
            return self._set_labels(issue_info['url'],
                                    issue_info['title'],
                                    issue_info['body'], False)

    def _set_labels(self, issue_url, title, body, label_comments):
        text = title + " " + body

        if label_comments:
            # add comments' body to issue's text
            r = self._session.get(issue_url + '/comments')
            for comm in r.json():
                text += ' ' + comm['body']

        labels = []

        for rule, label_text in zip(self._label_rules, self._label_list):
            if re.search(rule, text):
                labels.append(label_text)

        logging.debug(10 * '-')
        logging.debug('Issue url:', issue_url)
        logging.debug('Issue title:', title)

        if not labels:
            labels.append(self.default_label)

        logging.debug("Labeled as:", labels)

        r = self._session.post(issue_url + '/labels', data=json.dumps(labels))
        logging.debug('Status code:', r.status_code)

        return [labels, r.status_code]