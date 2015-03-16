#!/usr/bin/env python
import web
import json
import os
import random
from templatecache import TemplateCache
import urllib
import subprocess
import shlex
import textwrap
import settings
import datetime
import databaseconnect

" Load Data "
with open("./data/data.json") as f:
    meps = json.load(f)

db = databaseconnect.connect(settings.DATABASE_URL)

tc = TemplateCache()

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

def create_error(wi,ms=""):
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
            return "This MEP is not %s"%(ms if ms else "in our database")
        elif country and group:
            return "No MEP of group %s in country %s %s"%(group,country,ms)
        else:
            return "No MEP %s found :/"%(ms)


class Fax:
    """ Handle the Fax Widget """
    def GET(self):
        """ display the fax widget """
        web.header("Content-Type", "text/html;charset=utf-8")
        template = tc.get("fax.tmpl")
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
        db.query(u"""INSERT INTO faxes (message, faxnr, create_date) 
            VALUES ($m,$f,$d)""",
                vars = {
                "m" : textwrap.fill(args['body'],replace_whitespace=False),
                "f" : fax,
                "d" : datetime.datetime.now()})
        template = tc.get("fax-sent.tmpl")
        web.header("Content-Type", "text/html;charset=utf-8")
        return template.render(m)

class Tweet:
    def GET(self):
        """display the tweet widget"""
        ff = get_filter(web.input())
        web.header("Content-Type","text/html;charset=utf-8")
        template = tc.get("tweet.tmpl")
        m = weighted_choice(lambda x: x.get('twitter',None) and ff(x))
        if not m:
            return create_error(web.input(),"using Twitter")
        return template.render(m)

class mail:
    """ Handle Requests for Mail """
    def GET(self):
        """ Handle GET Requests """
        web.header("Content-Type", "text/html;charset=utf-8")
        template = tc.get("mail.tmpl")
        m = weighted_choice(get_filter(web.input()))
        if not m:
            return create_error(web.input())
        return template.render(m)

urls = ('/mail/', 'mail',
        '/fax/', 'Fax',
        '/tweet/','Tweet',)

web.config.debug = settings.DEVELOPMENT
app = web.application(urls,globals())

if __name__ == "__main__":
#    if not settings.TEST:
#        pid = os.fork()
#    else:
#        pid = None
#    if not pid:
#        app.run()
#    else:
#        with open(".pid","wb") as f:
#            f.write(str(pid))
    if not settings.DEVELOPMENT:
        web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()

