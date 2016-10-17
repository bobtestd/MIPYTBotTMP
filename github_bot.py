import requests
import json
import configparser
import re


class GitHubBot:
    def __init__(self, auth_file, label_file, url, period, default_label):
        self._read_config(auth_file, label_file)

        self.url = url
        self.period = period
        self.default_label = default_label

        self._session = requests.Session()
        self._session.headers = {'Authorization': 'token ' + self._token, 'User-Agent': 'Python'}

    def _read_config(self, auth_file, label_file):
        conf = configparser.ConfigParser()
        conf.read([auth_file, label_file])

        self._token = conf['github']['token']

        self._label_list = list(map(str.strip, conf['list']['labels'].split(',')))
        print("List of defined labels:", self._label_list)

        self._label_rules = []
        for label in self._label_list:
            self._label_rules.append(conf['rules'][label])

    def label_issues(self, label_comments):
        r = self._session.get(self.url)
        r.raise_for_status()

        for issue_info in r.json():
            if issue_info['labels']:
                continue

            self._set_labels(issue_info['number'], issue_info['title'], issue_info['body'], label_comments)

    def _set_labels(self, issue_num, title, body, label_comments):
        issue_url = self.url + '/' + str(issue_num)
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

        print(10 * '-')
        print('Issue number:', issue_num)
        print('Issue title:', title)
        print('Issue url:', issue_url)

        if not labels:
            labels.append(self.default_label)

        print("Labeled as:", labels)

        r = self._session.post(issue_url + '/labels', data=json.dumps(labels))
        print('Status code:', r.status_code)

