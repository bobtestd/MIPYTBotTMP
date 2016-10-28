# MIPYTGitHubBot
GitHub Issues Bot for MI-PYT in FIT CTU in Prague. The program has two modes: console and web app. In *console* mode it labels issues (checks new one with the specified frequency) in the given repository by the issues itself and their comments, and in *web* mode the program labels new opened issue as soon as possible (by [webhook](https://developer.github.com/webhooks/) notification and so one by one). 

### Requirements
* python 3.5
* libraries: [markdown](https://pypi.python.org/pypi/Markdown), [click](http://click.pocoo.org/6/), [requests](http://docs.python-requests.org/en/master/), [flask](http://flask.pocoo.org/), [appdirs](https://pypi.python.org/pypi/appdirs)

### Manual
Install package by typing the command: **python -m pip install --extra-index-url https://testpypi.python.org/pypi githubissuesbot**

Then you may run the app by typing **python -m githubissuesbot** or just **githubissuesbot**. Type **--help** for command line manual.

Read how to generate configuration files by typing **python -m githubissuesbot genconf --help** or **githubissuesbot genconf --help**.

The app requires the following configuration files: **auth.cfg** (with GitHub personal access token), **label.cfg** (with available labels and the appropriate rules as regular expressions), **secret.cfg** (with [webhook secret token](https://developer.github.com/webhooks/securing/)) and **web.cfg** (web app uses it for reading info about other configuration files).

If you want to deploy this app on some host (tested on [pythonanywhere](https://www.pythonanywhere.com/)), don't forget to manually fix **web_config_file** value in **web_app.py** on line 39.

Link to [testpypi](https://testpypi.python.org/pypi/githubissuesbot).


