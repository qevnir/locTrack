# locTrack

## Requirements

- Spatialite on Debian/Ubuntu:

 $ sudo apt install libsqlite3-mod-spatialite

- GDAL on Debian/Ubuntu:

$ sudo apt install libgdal-dev

- Install npm and nodejs:

$ sudo apt install nodejs npm


Install pip:
https://pip.pypa.io/en/stable/installation/

Run the following commands from the root directory:

$ make venv
$ source venv/bin/activate
$ make install

## Running for development

First run
$ source venv/bin/activate
$ make rundjango

then in a new terminal:
$ make runnpm