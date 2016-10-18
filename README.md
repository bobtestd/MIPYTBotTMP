# MIPYTGitHubBot
GitHub Issues Bot for MI-PYT in FIT CTU in Prague. The program has two modes: console and web app. In *console* mode it labels issues (checks new one with the specified frequency) in the given repository by the issues itself and their comments, and in *web* mode the program labels new opened issue as soon as possible (by [webhook](https://developer.github.com/webhooks/) notification and so one by one). 

### Requirements
* python 3.5
* libraries: [click](http://click.pocoo.org/6/), [requests](http://docs.python-requests.org/en/master/), [json](http://docs.python.org/3.5/library/json.html), [configparser](http://docs.python.org/3.5/library/configparser.html), [re](http://docs.python.org/3.5/library/re.html), [sched](http://docs.python.org/3.5/library/sched.html), [time](http://docs.python.org/3.5/library/time.html), [flask](http://flask.pocoo.org/), [hashlib](https://docs.python.org/3/library/hashlib.html), [hmac](https://docs.python.org/3/library/hmac.html), [logging](https://docs.python.org/3/library/logging.html)

### Manual
First, create **auth.cfg** (with GitHub token), **label.cfg** (with available labels and the appropriate rules as regular expressions), **secret.cfg** (with [webhook secret token](https://developer.github.com/webhooks/securing/)) and **web.cfg** (web app uses it for reading info about configuration files) files with the same structure as in **./config** directory.

Then you may run python directly on archived package with sources (not multiple attachments/archives, so "archive/sources_files" is valid and "archive/some_dir/sources_files" is not).

Type --help for command line manual.
