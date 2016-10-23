from setuptools import setup, find_packages


long_description = ''

try:
    import pypandoc
    from pypandoc.pandoc_download import download_pandoc

    download_pandoc()

    pypandoc.convert_file('README.md', 'rst', outputfile='README.rst')
    with open('README.rst', 'r') as file:
        long_description = file.read()
except (ImportError,RuntimeError) as e:
    print('Warning: ' + str(e) + ': could not convert Markdown to RST.')

    with open('README.txt', 'w') as file_out:
        with open('README.md', 'r') as file_in:
            long_description = file_in.read()
            file_out.write(long_description)

setup(
    name='githubissuesbot',
    version='0.3',
    description='GitHub issues bot as console and web app.',
    long_description=long_description,
    author='Dmitriy Bobir',
    author_email='astercassio@gmail.com',
    url='https://github.com/bobirdmi',
    keywords='github,bot,issues',
    license='Public Domain',
    packages=find_packages(),
    setup_requires=['pypandoc>=1'],
    install_requires=['Flask', 'markdown>=2', 'click>=6', 'requests>=2', 'appdirs>=1'],
    entry_points={
            'console_scripts': [
                'githubbot = githubissuesbot.command_line:main',
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