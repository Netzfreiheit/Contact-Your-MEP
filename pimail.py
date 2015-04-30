#!/usr/bin/env python
import web
import json
import os
import random
from templatecache import TemplateCache
import urllib
import textwrap
import settings
import datetime
import databaseconnect
import logger

" Load Data "
with open("./data/data.json") as f:
    meps = json.load(f)
    mep_by_id = {m['id']: m for m in meps}

db = databaseconnect.connect(settings.DATABASE_URL)

tc = TemplateCache()

def weighted_choice(ff=lambda x: x, type="fax"):
    """ Pick a MEP based on the score weight """
    lm = filter(ff, meps)
    ts = sum(i['score'] for i in lm)
    r = random.uniform(0, ts)
    n = 0
    for c in lm:
        n = n + c['score']
        if n > r and (type != 'fax' or (not c.get('fax_optout') and c.get('fax_bxl'))):
            return c
    return False

def decode_args(a):
    return {k: urllib.unquote_plus(v).decode("utf-8")
            for k, _, v in (i.partition("=") for i in a.split("&"))}

def get_filter(wi):
    country = getattr(wi, 'country', None)
    group = getattr(wi, 'group', None)
    id = getattr(wi, 'id', None)

    if id:
        return lambda x: x.get('id') == id
    if country and group:
        return lambda x: x.get('country_short') == country and x.get('group_short') == group
    if country:
        return lambda x: x.get('country_short') == country
    if group:
        return lambda x: x.get('group_short') == group
    return lambda x: x

def create_error(wi, ms=""):
    country = getattr(wi, 'country', None)
    group = getattr(wi, 'group', None)
    id = getattr(wi, 'id', None)

    if id:
        return "This MEP is not %s" % (ms if ms else " available with this contact method")
    if country and group:
        return "No MEP of group %s in country %s %s" % (group, country, ms)
    return "No MEP %s found :/" % ms


class Fax:
    """ Handle the Fax Widget """
    def GET(self):
        """ display the fax widget """
        web.header("Content-Type", "text/html;charset=utf-8")
        template = tc.get("fax.tmpl")
        m = weighted_choice(get_filter(web.input()), 'fax')
        if not m:
            return create_error(web.input())
        return template.render(m)

    def POST(self):
        "send out the fax"
        args = decode_args(web.data())
        m = mep_by_id[args['id']]
        if settings.TEST:
            fax = '100'
        else:
            fax = m[settings.FAX_FIELD].replace(" ", "").replace("+", "00")
        db.query(u"""INSERT INTO faxes (message, faxnr, create_date, campaign_id) 
            VALUES ($m,$f,$d,$s)""",
                vars = {
                "m" : textwrap.fill(args['body'],replace_whitespace=False).replace('<','&lt;').replace('>','&gt;'),
                "f" : fax,
                "d" : datetime.datetime.now(),
                's' : settings.campaign_id})
        template = tc.get("fax-sent.tmpl")
        web.header("Content-Type", "text/html;charset=utf-8")
        return template.render(m)

class Tweet:
    def GET(self):
        """display the tweet widget"""
        ff = get_filter(web.input())
        web.header("Content-Type", "text/html;charset=utf-8")
        template = tc.get("tweet.tmpl")
        m = weighted_choice(lambda x: x.get('twitter') and ff(x), 'tweet')
        if not m:
            return create_error(web.input(), "using Twitter")
        return template.render(m)

class Subscribe:
    def GET(self):
        """subscribe to newsletter"""
        web.header("Content-Type", "application/javascript;charset=utf-8")
        web.header("Access-Control-Allow-Origin", "*")
        wi = web.input()
        if hasattr(wi, 'mail'):
            mail = wi.mail
        else:
            return """{status: 'error',
                     message: 'no mail'}"""
        country = wi.country if hasattr(wi, 'country') else ""
        logger.log(db, mail, country)
        return """{status: 'success',
                   message: 'logged mail %s from country %s'
                   }""" % (mail, country)


class mail:
    """ Handle Requests for Mail """
    def GET(self):
        """ Handle GET Requests """
        web.header("Content-Type", "text/html;charset=utf-8")
        template = tc.get("mail.tmpl")
        m = weighted_choice(get_filter(web.input()), 'mail')
        if not m:
            return create_error(web.input())
        return template.render(m)

urls = ('/' + settings.campaign_path + '/mail/', 'mail',
        '/' + settings.campaign_path + '/fax/', 'Fax',
        '/' + settings.campaign_path + '/subscribe/', Subscribe,
        '/' + settings.campaign_path + '/tweet/', 'Tweet',)

web.config.debug = settings.DEVELOPMENT
app = web.application(urls, globals())

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

