import web
import json
import random
from jinja2 import Template
import urllib

" Load Data "
with open("data.json") as f:
    meps = json.load(f)
    total_score = sum((i['score'] for i in meps))

def weighted_choice(a):
    """ Pick a MEP based on the score weight """
    r = random.uniform(0,total_score)
    n = 0
    for c in a:
        n = n + c['score']
        if n>r:
            return c
    return False


class Fax:
    """ Handle the Fax Widget """
    
    def GET(self):
        """ display the fax widget """
        web.header("Content-Type", "text/html;charset=utf-8")
        with open("fax.tmpl") as f:
            template = Template(f.read().decode("utf-8"))
        m = weighted_choice(meps)
        return template.render(m)
    def POST(self):
        "send out the fax"
        print web.data()
        return self.GET()


class mail:
    """ Handle Requests for Mail """
    def GET(self):
        """ Handle GET Requests """
        web.header("Content-Type", "text/html;charset=utf-8")
        with open("mail.tmpl") as f:
            template = Template(f.read().decode("utf-8"))
        m = weighted_choice(meps)
        return template.render(m)

urls = ('/widget/', 'mail',
        '/widget/fax/', 'Fax')

app = web.application(urls,globals())

if __name__ == "__main__":
    app.run()
