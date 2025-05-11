from setuptools import setup, find_packages
import time

time.sleep(10)

setup(
    name='ctftestsowwy',
    version='7.1',
    packages=find_packages(),
    install_requires=[
        'RestrictedPython',
    ]
)

