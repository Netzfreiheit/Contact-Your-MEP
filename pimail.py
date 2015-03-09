import web
import json
import os
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

def weighted_choice(ff=lambda x: x):
    """ Pick a MEP based on the score weight """
    lm = filter(ff,meps)
    ts = sum((i['score'] for i in lm))
    r = random.uniform(0,ts)
    n = 0
    for c in lm:
        n = n + c['score']
        if n>r and c.get('fax_bxl',None):
            return c
    return False

def unquote(a):
    return (a[0],unicode(urllib.unquote_plus(a[1]).decode("utf-8")))

def decode_args(a):
    return dict((unquote(i.split("=")) for i in a.split("&")))

def get_mep_by_id(id):
    for m in meps:
        if m['id']==id:
            return m
    return None

def get_filter(wi):
        if hasattr(wi,'country'):
            country = wi.country
        else:
            country = None
        if hasattr(wi,'group'):
            group = wi.group
        else:
            group = None
        if hasattr(wi, 'id'):
            id = wi.id
        else:
            id = None
        if id:
            ff = lambda x: x.get('id',None) == id
        elif country and group:
            ff = lambda x: x.get('country_short',None) == country and x.get('group_short',None) == group
        elif country:
            ff = lambda x: x.get('country_short',None) == country
        elif group:
            ff = lambda x: x.get('group_short',None) == group
        else:
            ff = lambda x: x
        return ff

def create_error(wi):
        if hasattr(wi,'country'):
            country = wi.country
        else:
            country = None
        if hasattr(wi,'group'):
            group = wi.group
        else:
            group = None
        if hasattr(wi, 'id'):
            id = wi.id
        else:
            id = None
        if id:
            return "No MEP with this id"
        elif country and group:
            return "No MEP of group %s in country %s"%(group,country)
        else:
            return "No MEP found :/"
    

class Fax:
    """ Handle the Fax Widget """
    def GET(self):
        """ display the fax widget """
        web.header("Content-Type", "text/html;charset=utf-8")
        with open("fax.tmpl") as f:
            template = Template(f.read().decode("utf-8"))
        m = weighted_choice(get_filter(web.input()))
        if not m:
            return create_error(web.input())
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
        ff = get_filter(web.input())
        web.header("Content-Type","text/html;charset=utf-8")
        with open("tweet.tmpl") as f:
            template = Template(f.read().decode("utf-8"))
        if not m:
            return create_error(web.input())
        m = weighted_choice(lambda x: x.get('twitter',None) and ff(x))
        return template.render(m)

class mail:
    """ Handle Requests for Mail """
    def GET(self):
        """ Handle GET Requests """
        web.header("Content-Type", "text/html;charset=utf-8")
        with open("mail.tmpl") as f:
            template = Template(f.read().decode("utf-8"))
        if not m:
            return create_error(web.input())
        m = weighted_choice(get_filter(web.input()))
        return template.render(m)

urls = ('/widget/', 'mail',
        '/widget/fax/', 'Fax',
        '/widget/tweet/','Tweet',)

app = web.application(urls,globals())

if __name__ == "__main__":
    if not settings.TEST:
        pid = os.fork()
    else:
        pid = None
    if not pid:
        app.run()
    else:
        with open(".pid","wb") as f:
            f.write(str(pid))

