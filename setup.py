# This is a script that tells pip how to setup your
# code on the system. You don't need to make any
# changes to it, nor do you need to call it yourself.
# pip runs it for you when you type commands.

from setuptools import setup
import os
import codecs
import re

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


# Get the long description from the README file
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

user_info_m = re.search(
    r":Implemented By:\s+((?:\w+\s?)+)\s*<(\w+)@([\w.]+)>",
    long_description,
    re.DOTALL)

if not user_info_m:
    raise ValueError("Please stick to the ``Full Name <user@domain>`` format")
name, user, domain = user_info_m.groups()

deliv_m = re.search(
    r":Deliverable:\s*(\d+)",
    long_description,
    re.DOTALL)

if not deliv_m:
    raise ValueError("Could not find what deliverable you are working on")
deliv = int(deliv_m.group(1))

setup(
    name='slytherlisp-{}'.format(user),
    version='1.0.{}-devel'.format(deliv),

    description='Scheme like programming language for CSCI-400 at Mines',
    long_description=long_description,

    url='https://lambda.mines.edu',

    author=name,
    author_email='{}@{}'.format(user, domain),

    license='Closed source; do not share with other students '
            'in (or who will be in) this course.',

    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='scheme',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['slyther'],

    python_requires='>=3.5, <4',

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['flake8', 'flake8-pep3101'],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'slyther=slyther.__main__:main',
        ],
    },
)
