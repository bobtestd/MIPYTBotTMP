import requests
import json
import configparser
import re
import logging


logging.basicConfig(filename='github_bot.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


class GitHubBot:
    def __init__(self, auth_file, label_file, url, default_label):
        """
        A constructor.

        :param auth_file: path to file with authorization info.
        :param label_file: path to file with issue labels and their rules.
        :param url: Url of issues in repo (ex.: https://api.github.com/repos/<username>/<repo>/issues).
        If you want to label ALL issues in this repo, you MUST specify this parameter. Otherwise,
        set it to None in case of labeling only one issue.
        :param default_label: If no rule can be applied to issue, an issue will be labeled by this string.
        """
        self._read_config(auth_file, label_file)

        self.url = url
        self.default_label = default_label

        self._session = requests.Session()
        self._session.headers = {'Authorization': 'token ' + self._token, 'User-Agent': 'Python'}

    def _read_config(self, auth_file, label_file):
        conf = configparser.ConfigParser()
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

        for issue_info in r.json():
            if issue_info['labels']:
                continue

            self._set_labels(self.url + '/' + str(issue_info['number']),
                             issue_info['title'],
                             issue_info['body'], label_comments)

    def label_issue(self, issue_info):
        if not issue_info['labels']:
            self._set_labels(issue_info['url'],
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
