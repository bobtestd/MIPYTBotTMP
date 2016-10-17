# MIPYTGitHubBot
GitHub Issues Bot for MI-PYT in FIT CTU in Prague. The program labels issues in the given repository by the issues itself and their comments.

### Requirements
* python 3.5
* libraries: [click](http://click.pocoo.org/6/), [requests](http://docs.python-requests.org/en/master/), [json](http://docs.python.org/3.5/library/json.html), [configparser](http://docs.python.org/3.5/library/configparser.html), [re](http://docs.python.org/3.5/library/re.html), [sched](http://docs.python.org/3.5/library/sched.html), [time](http://docs.python.org/3.5/library/time.html)

### Manual
First, create **auth.cfg** (with GitHub token) and **label.cfg** (with available labels and the appropriate rules as regular expressions) files with the same structure as in **./config** directory.

Then you may run python directly on archived package with sources (not multiple attachments/archives, so "archive/sources_files" is valid and "archive/some_dir/sources_files" is not).

Type --help for command line manual.
