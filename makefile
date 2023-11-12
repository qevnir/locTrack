.PHONY: install
install: activate install-python install-npm

venv:
	python3 -m venv venv

install-python:
	pip install -r requirements.txt

install-npm:
	npm install

rundjango:
	python3 locTrack/manage.py runserver

runnpm:
	cd locTrack-app/ && npm run serve


clean:
	rm -rf venv
