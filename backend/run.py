from __future__ import unicode_literals

from flask import Flask
from flask import render_template
app = Flask(__name__)

# Entry point: View all faxes as list
@app.route('/')
def list():
    return render_template('list_view.html')

if __name__ == '__main__':
    app.debug = True
    app.run()