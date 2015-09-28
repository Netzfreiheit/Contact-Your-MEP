# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask
from flask import render_template

app = Flask(__name__)

data = [
    {
        "id": 1,
        "created": "2015-02-02",
        "modified": "2015-02-18",
        "text": "asdpjsapdo oaisj füjfds aüsdijf aüosdifj aüosdijf aosidf jaüsoidjf üaoisdf",
        "checked": False,
        "sent": False
    },
    {
        "id": 2,
        "created": "2015-02-02",
        "modified": "2015-02-18",
        "text": "asdpjsapdo oaisj füjfds aüsdijf aüosdifj aüosdijf aosidf jaüsoidjf üaoisdf",
        "checked": True,
        "sent": True
    }

]

# Entry point: View all faxes as list
@app.route('/')
def list():
    return render_template('list_view.html', data=data)

@app.route('/edit/<id_>')
def edit(id_):
    return render_template('edit.html', fax=data[int(id_)])

if __name__ == '__main__':
    app.debug = True
    app.run()