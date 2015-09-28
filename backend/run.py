# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask
from flask import render_template
app = Flask(__name__)

# Entry point: View all faxes as list
@app.route('/')
def list():
    data = [
        {
            "text": "asdpjsapdo oaisj füjfds aüsdijf aüosdifj aüosdijf aosidf jaüsoidjf üaoisdf",
            "checked": False,
            "sent": False
        },
        {
            "text": "asdpjsapdo oaisj füjfds aüsdijf aüosdifj aüosdijf aosidf jaüsoidjf üaoisdf",
            "checked": True,
            "sent": True
        }

    ]
    return render_template('list_view.html', data=data)

if __name__ == '__main__':
    app.debug = True
    app.run()