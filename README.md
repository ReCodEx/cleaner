# Cleaner

[![License](http://img.shields.io/:license-mit-blue.svg)](http://badges.mit-license.org)
[![Docs](https://img.shields.io/badge/docs-latest-brightgreen.svg)](http://recodex.github.io/cleaner/)
[![Wiki](https://img.shields.io/badge/docs-wiki-orange.svg)](https://github.com/ReCodEx/wiki/wiki)
[![GitHub release](https://img.shields.io/github/release/recodex/cleaner.svg)](https://github.com/ReCodEx/wiki/wiki/Changelog)
[![COPR](https://copr.fedorainfracloud.org/coprs/semai/ReCodEx/package/recodex-cleaner/status_image/last_build.png)]()

Cleaner component is tightly bound to the worker. It manages the cache folder of
the worker, mainly deletes outdated files. Every cleaner instance maintains one
cache folder, which can be used by multiple workers. This means on one server
there can be numerous instances of workers with the same cache folder, but there
should be only one cleaner instance.

Cleaner is written in Python 3 programming language, so it works well
multi-platform. It uses only `pyyaml` library for reading configuration file and
`argparse` library for processing command line arguments.

It is a simple script which checks the cache folder, possibly deletes old files
(based on last modification times) and then ends. This means that the cleaner has
to be run repeatedly, for example using cron, systemd timer or Windows task
scheduler. For proper function of the cleaner a suitable cron interval has to
be used. It is recommended to use 24 hour interval which is sufficient enough for
intended usage. The value is set in the configuration file of the cleaner.

## How to run it

Whole cleaner is written in `python` and uses version 3 features. If version 3 is default on machine simple `python` command can be used.

- install `python3` and `pip3` according to your OS
- install dependencies using `pip3 install -r requirements.txt`
- run app with `python3 ./main.py -c ./cleaner/install/config.yml`, without specifying config file cleaner will not work

## Installation

### COPR Installation

Follows description for CentOS which will do all steps as described in _Manual Installation_.

```
$ yum install yum-plugin-copr
$ yum copr enable semai/ReCodEx
$ yum install recodex-cleaner
```

### Manual Installation

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

### Configuration

The default location for cleaner configuration file is
`/etc/recodex/cleaner/config.yml`.

#### Configuration items

- **cache-dir** -- directory which cleaner manages
- **file-age** -- file age in seconds which is considered as outdated and will
   be marked for deletion

#### Example configuration

```{.yml}
cache-dir: "/tmp"
file-age: "3600"  # in seconds
```

### Execution

As stated before cleaner should be croned, on linux systems this can be done by
built in `cron` service or if there is `systemd` present cleaner itself provides
`*.timer` file which can be used for croning from `systemd`. On Windows systems
internal scheduler should be used.

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

Cron on Windows is provided by `Task Scheduler`. This can be done using GUI interface or with command line, command line description follows:

- start `cmd` as administrator
- find your `recodex-cleaner` installation on your filesystem, `C:\Program Files\ReCodEx\cleaner` will be used as demonstrative
- execute following command `schtasks /create /sc daily /tn "ReCodEx Cleaner" /tr "\"C:\Program Files\ReCodEx\cleaner\recodex-cleaner.exe\" -c \"C:\Program Files\ReCodEx\cleaner\config.yml\""`
- this will create task named `ReCodEx Cleaner` which will be executed daily on time of creation

## Documentation

Feel free to read the documentation on [our wiki](https://github.com/ReCodEx/wiki/wiki).
