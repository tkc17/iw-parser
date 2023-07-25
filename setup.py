import re
import subprocess

from setuptools import setup, find_packages
# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    version="0.0.1",
    long_description=long_description,
    long_description_content_type='text/markdown'
)