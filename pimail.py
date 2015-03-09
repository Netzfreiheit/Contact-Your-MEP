import web
import json
import random
from jinja2 import Template
import urllib
import subprocess
import shlex
import textwrap
import settings

" Load Data "
with open("./data/data.json") as f:
    meps = json.load(f)
    total_score = sum((i['score'] for i in meps))

def weighted_choice(a):
    """ Pick a MEP based on the score weight """
    r = random.uniform(0,total_score)
    n = 0
    for c in a:
        n = n + c['score']
        if n>r and c.get('fax',None):
            return c
    return False

def unquote(a):
    return (a[0],unicode(urllib.unquote_plus(a[1]).decode("utf-8")))

def decode_args(a):
    return dict((unquote(i.split("=")) for i in a.split("&")))

def get_mep_by_id(id):
    for m in meps:
        if m['id']==int(id):
            return m
    return None

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
        args=decode_args(web.data())
        m = get_mep_by_id(args['id'])
        if settings.TEST:
            fax = '100'
        else:
            fax = m[settings.FAX_FIELD].replace(" ","").replace("+","00")
        with open("fax-out.tmpl") as f:
            template = Template(f.read().decode("utf-8"))
        data = {"body": textwrap.fill(args['body'],replace_whitespace=False),
                "from": settings.FROM,
                "to": "%s@%s" % (fax, settings.FAX_GATEWAY),
                }
        a = shlex.split(settings.SENDMAIL)
        " add the recipient as args "
        a.append("%s@%s" % (fax,settings.FAX_GATEWAY))
        p = subprocess.Popen(a,
                             stdin=subprocess.PIPE)
        p.communicate(template.render(data).encode("iso-8859-1","replace"))
        
        with open("fax-sent.tmpl") as f:
            template = Template(f.read().decode("utf-8"))
        web.header("Content-Type", "text/html;charset=utf-8")
        return template.render(m)

class Tweet:
    def GET(self):
        """display the tweet widget"""
        web.header("Content-Type","text/hmtl;charset=utf-8")
        with open("tweet.tmpl") as f:
            template = Template(f.read().decode("utf-8"))
        m = weighted_choice(meps)
        return template.render(m)

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
