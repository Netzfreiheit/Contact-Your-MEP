import web
import json
from jinja2 import Template
import random


with open("widget.tmpl") as f:
    template = Template(f.read().decode("utf-8"))

with open("data.json") as f:
    meps = json.load(f)

class mail:
    def GET(self):
        web.header("Content-Type", "text/html;charset=utf-8")
        with open("widget.tmpl") as f:
            template = Template(f.read().decode("utf-8"))
        m = random.choice(meps)
        return template.render(m)

urls = ('/', 'mail' )

app = web.application(urls,globals())

if __name__ == "__main__":
    app.run()
