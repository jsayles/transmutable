
# Transmutable: Tools for working in public

This project provides tools for people who run their work life out in the open.

You can see it in action at [transmutable.com](http://transmutable.com/).

Questions and comments sent to Trevor F. Smith at trevor@transmutable.com will be answered as time permits.

This is not an off-the-shelf product and it requires someone who knows how to configure and manage Django web projects.

## Colophon:

1. Markdown 
1. Python
1. Django
1. South

## Installation:

	pip -r requirements.txt
	cp local_settings.example local_settings.py
	# Follow instructions in local_settings.py
	./manage.py syncdb
	./manage.py migrate

## Try it out:

	./manage.py install_demo # Note, this deletes records in the DB and creates example accounts 
	./manage.py runserver 0.0.0.0:8000
	# open http://127.0.0.1:8000/
