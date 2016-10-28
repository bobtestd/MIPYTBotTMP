import click
from . import github_bot
from . import web_app
import sched
import time
import appdirs
import pkg_resources
import os


app_name = __name__.split('.')[0]


@click.group()
def cli():
    pass


@cli.command()
@click.option('-d', '--directory', default='./',
              help='Set directory the web config files will be created in. '
                   'Default directory: ./')
def genconf(directory):
    """Generate sample web config files"""
    os.makedirs(os.path.dirname(directory + '/somefile.example'), exist_ok=True)
    click.echo('Generating sample web config files...')
    create_web_config(directory, 'label.cfg')
    create_web_config(directory, 'auth.cfg.sample')
    create_web_config(directory, 'secret.cfg.sample')
    create_web_config(directory, 'web.cfg.sample')
    click.echo('Done')


@cli.command()
@click.option('-c', '--config',
              help='Set path to a file with web configuration. '
                   'Default path: ' + appdirs.site_config_dir(appname=app_name) + '/web.cfg')
def web(config):
    """Run the web app"""
    web_app.run_local_web(config)


@cli.command()
@click.argument('auth_file', type=click.Path(exists=True))
@click.argument('label_file', type=click.Path(exists=True))
@click.option('-u', '--user', prompt='Username', help='Username of repository owner.')
@click.option('-r', '--repo', prompt='Repo', help='This repository will be processed.')
@click.option('-p', '--period', default=30,
              help='How often issues in the given repository will be processed and labeled (in seconds). '
                   'By default is 30.')
@click.option('-l', '--deflabel', default='default',
              help='Default label for those issues that do not satisfy any rules in the label_file. '
                   'By default is "default".')
@click.option('-c', '--comments', is_flag=True, help='Set this option if the program must use comments for labeling.')
def console(auth_file, label_file, user, repo, period, deflabel, comments):
    """Run the console app"""
    click.echo('Running the console app')
    print(10 * '=')

    url = 'https://api.github.com/repos/' + user + '/' + repo + '/issues'
    bot = github_bot.GitHubBot(click.format_filename(auth_file),
                               click.format_filename(label_file),
                               url, deflabel)

    my_scheduler = sched.scheduler(time.time, time.sleep)

    def repeated_labeling(sc):
        bot.label_all_issues(comments)

        print(10 * '=')
        print("Labeling in", period, "seconds...")
        my_scheduler.enter(period, 1, repeated_labeling, (sc,))

    my_scheduler.enter(0, 1, repeated_labeling, (my_scheduler,))
    my_scheduler.run()


def create_web_config(new_dir, filename):
    with open(new_dir + '/' + filename, 'wb') as f:
        f.write(pkg_resources.resource_string(app_name, '/config/' + filename))


def main():
    cli(prog_name=app_name)