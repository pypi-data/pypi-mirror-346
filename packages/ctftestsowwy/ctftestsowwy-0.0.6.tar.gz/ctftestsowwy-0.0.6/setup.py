from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        print('HIIII HELOOODEVELOP')

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        print('HIIII HELOOO')

def RunCommand():
    #print('HELOOOOO\n'*88   )
    print("Hello, p0wnd!")

class RunEggInfoCommand(egg_info):
    def run(self):
        RunCommand()
        egg_info.run(self)


class RunInstallCommand(install):
    def __init__(self):
        print('YOOOOOOOO!')
    def run(self):
        RunCommand()
        install.run(self)


setup(
    name = "ctftestsowwy",
    version = "0.0.6",
    license = "MIT",
    packages=find_packages(),
    cmdclass={
        'install' : RunInstallCommand,
        'egg_info': RunEggInfoCommand,
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)   