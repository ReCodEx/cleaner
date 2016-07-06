#!/usr/bin/env python3

from setuptools import setup
import sys
from cleaner import __version__

if sys.platform == "win32":
    files=[]
else:
    files=[
        ('/etc/systemd/system', ['install/recodex-cleaner.service', 'install/recodex-cleaner.timer']),
        ('/etc/recodex/cleaner', ['install/config.yml'])
        ]

setup(name='recodex-cleaner',
      version=__version__,
      description='Clean cache which is used by ReCodEx workers',
      author='ReCodEx Team',
      author_email='',
      url='https://github.com/ReCodEx/cleaner',
      license="MIT",
      keywords=['ReCodEx', 'cleaner', 'cache'],
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   'Operating System :: OS Independent',
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5"],
      packages=['cleaner'],
      data_files=files,
      entry_points={'console_scripts': ['recodex-cleaner = cleaner.main:main']}
      )
