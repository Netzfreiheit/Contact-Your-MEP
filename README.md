pimail - Mailwidget for the EP
==============================

Find a random MEP and write a mail in your browser (then works through a
mailto: link)

Installation
============

pimail depends on:

* web.py
* Jinja2

install with ``pip install web.py jinja2``

Edit the widget.tmpl and files in static/ to your liking

Fill data.json with an array of data about the MEPs (or MPs or whatever)

and start with: ``python pimail.py``

this will run a webserver on port 8080

For server integration: I do use mod_proxy and point the /static/
subsection to files (not having it served through web.py).


