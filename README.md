# Cleaner

[![License](http://img.shields.io/:license-mit-blue.svg)](http://badges.mit-license.org)
[![Docs](https://img.shields.io/badge/docs-latest-brightgreen.svg)](http://recodex.github.io/cleaner/)
[![Wiki](https://img.shields.io/badge/docs-wiki-orange.svg)](https://github.com/ReCodEx/GlobalWiki/wiki)

Cleaner is script which should be cronned on machine on which worker is deployed. Its function is continuously delete cache folder from old files which are no longer used. To efectively do this filesystem should be able to display last access time.

## Enable last access timestamp

**Linux:**

- open `/etc/fstab` as administrator
- filesystem which will be used as `ReCodEx` cache has to have `strictatime` option specified
- more on this subject can be found [here](https://en.wikipedia.org/wiki/Stat_%28system_call%29#Criticism_of_atime)

**Windows:**

- start `cmd` with administrator permissions
- run following command `fsutil behavior set disablelastaccess 0`
- restart computer and last time access timestamps should be functional

## How to run it

Whole cleaner is written in `python` and uses version 3 features. If version 3 is default on machine simple `python` command can be used.

- install `python3` and `pip3` according to your OS
- install dependencies using `pip3 install -r requirements.txt`
- run app with `python3 ./main.py -c ./cleaner/install/config.yml`, without specifying config file cleaner will not work

## Installation

**Fedora (and other RPM distributions):**

- run `python3 setup.py bdist_rpm --post-install ./cleaner/install/postinst` to generate binary `.rpm` package
- install package using `sudo dnf install ./dist/recodex-cleaner-0.1.0-1.noarch.rpm` (depends on actual version)

**Other Linux systems:**

- run installation as `python3 setup.py install --install-scripts /usr/bin`
- run postinst script as root with `sudo ./cleaner/install/postinst`

**Windows:**

- start `cmd` with administrator permissions
- decide in which folder cleaner should be installed, `C:\Program Files\ReCodEx\cleaner` is assumed
- run installation with `python setup.py install --install-scripts "C:\Program Files\ReCodEx\cleaner"` where path specified with `--install-scripts` can be changed
- copy configuration file alongside with installed executable using `copy install\config.yml "C:\Program Files\ReCodEx\cleaner\config.yml"`

## Configuration and running

Generally there are two steps which has to be done to properly run cleaner service.

- editation of configuration file and setting up all things needed. **Note: Cache directory which will be cleaned should be same as for workers!**
- Setup cron to execute cleaner in given interval (once in a day should work)

**Linux (with systemd):**

Installation of `cleaner` contains `systemd` `*.timer` and `*.service` files which can be used to run it. Running through `systemd` is quite advised, because of prepared configuration.

- edit configuration file `/etc/recodex/cleaner/config.yml`
- run with systemd timer via `sudo systemctl start recodex-cleaner.timer`

**Linux (with cron):**

In case of manual execution, `cleaner` should be run using `cron` with some recommended interval.

- edit configuration file `/etc/recodex/cleaner/config.yml`
- edit crontab (`/etc/crontab`) and add following line: `0 0 * * * /usr/bin/recodex-cleaner -c /etc/recodex/cleaner/config.yml`
- given entry will run cleaner at 00:00 every day

**Windows:**

Cronning on Windows is provided by `Task Scheduler`. This can be done using GUI interface or with command line, command line description follows:

- start `cmd` as administrator
- find your `recodex-cleaner` installation on your filesystem, `C:\Program Files\ReCodEx\cleaner` will be used as demonstrative
- execute following command `schtasks /create /sc daily /tn "ReCodEx Cleaner" /tr "\"C:\Program Files\ReCodEx\cleaner\recodex-cleaner.exe\" -c \"C:\Program Files\ReCodEx\cleaner\config.yml\""`
- this will create task named `ReCodEx Cleaner` which will be executed daily on time of creation
