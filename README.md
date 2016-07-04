# Cleaner

[![License](http://img.shields.io/:license-mit-blue.svg)](http://badges.mit-license.org)
[![Docs](https://img.shields.io/badge/docs-latest-brightgreen.svg)](http://recodex.github.io/cleaner/)
[![Wiki](https://img.shields.io/badge/docs-wiki-orange.svg)](https://github.com/ReCodEx/GlobalWiki/wiki)

Cleaner is script which should be cronned on machine on which worker is deployed. Its function is continuously delete cache folder from old files which are no longer used. To efectively do this filesystem should be able to display last access time.

## Enable last access timestamp

**Linux:**

- TODO

**Windows:**

- TODO

## How to run it

Whole cleaner is written in `python` and uses version 3 features.

- install `python3` and `pip3` according to your OS
- install dependencies using `pip3 install -r requirements.txt`
- run app with `python3 ./main.py -c ./install/config.yml`, without specifying config file cleaner will not work

## Installation

**Fedora (and other RPM distributions):**

- run `python3 setup.py bdist_rpm --post-install ./install/postints` to generate binary `.rpm` package
- install package using `sudo dnf install ./dist/recodex-cleaner-0.1.0-1.noarch.rpm` (depends on actual version)

**Other Linux systems:**

- run installation as `python3 setup.py install --install-scripts /usr/bin`
- run postinst script as root with `sudo ./install/postinst`

**Windows:**

- TODO
- TODO

## Configuration and running

Installation of `cleaner` contains `systemd` `*.timer` and `*.service` files which can be used to run it. Running through `systemd` is quite advised, because of prepared configuration. In case of manual execution, `cleaner` should be run using `cron` with some reasonable interval (once in day should work).

- edit configuration file `/etc/recodex/cleaner/config.yml`. **Cache directory which will be cleaned should be same as for workers!**
- run with systemd timer via `sudo systemctl start recodex-cleaner.timer`
