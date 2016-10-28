from setuptools import setup, find_packages


with open('githubissuesbot/README.md', 'w') as file_out:
    with open('README.md', 'r') as file_in:
        file_out.write(file_in.read())

with open('README.rst', 'r') as file:
    long_description = file.read()

setup(
    name='githubissuesbot',
    version='0.3.2',
    description='GitHub issues bot as console and web app.',
    long_description=long_description,
    author='Dmitriy Bobir',
    author_email='astercassio@gmail.com',
    url='https://github.com/bobirdmi',
    keywords='github,bot,issues',
    license='Public Domain',
    packages=find_packages(),
    install_requires=['Flask', 'markdown>=2', 'click>=6', 'requests>=2', 'appdirs>=1'],
    entry_points={
            'console_scripts': [
                'githubissuesbot = githubissuesbot.command_line:main',
            ],
    },
    package_data={
            'githubissuesbot': [
                'config/*',
                'templates/*.html',
                'README.md'
            ],
    },
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        ],
)

