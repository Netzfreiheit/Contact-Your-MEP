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
import logger
import json
import GeoIP

" Load Data "
with open("./data/data.json") as f:
    meps = json.load(f)

    # calculate score sums per country
    mepCountryScores = {}
    mepTotalScore = 0
    mepCountryBias = 0.8 # we want 80% of hits to be from the user's own country
    for m in meps:
        country = m['country_short']
        if not country in mepCountryScores: mepCountryScores[country] = 0
	mepCountryScores[country] += m['score']
        mepTotalScore += m['score']

db = databaseconnect.connect(settings.DATABASE_URL)

tc = TemplateCache()

def lookupIp(ip=None):
    substitutions = {
        "gb": "uk"
    }
    rc = None

    # Get the web.py request IP if available (and no IP was provided explicitly)
    if ip == None and hasattr(web, 'ctx') and hasattr(web.ctx, 'ip'):
        ip = web.ctx.ip

    if ip != None:
        gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
        rc = gi.country_code_by_addr(ip)
        if rc != None: rc = rc.lower()

    if rc in substitutions:
        rc = substitutions[rc]

    return rc

def boostedScore(mep, country, factor=100):
    """ Multiply and return a candidate's score by a factor if its country matches the requested one """
    rc = mep['score']

    if mep['country_short'] == country:
        rc *= factor

    return rc

def getCountryFactor(country):
    """ Calculate the boost factor for a specific country (so that its MEPs will be picked (mepCountryBias*100)% of the time) """
    rc = 100 # default value in case the user's country wasn't found

    if country in mepCountryScores:
        countryScore = mepCountryScores[country]
        otherScore = mepTotalScore - countryScore
        rc = otherScore*mepCountryBias/(countryScore*(1-mepCountryBias))

    return rc

def weighted_choice(ff=lambda x: x, type="fax"):
    """ Pick a MEP based on the score weight """
    userCountry = lookupIp()
    factor = getCountryFactor(userCountry)

    lm = filter(ff,meps)
    ts = sum((boostedScore(i, userCountry, factor) for i in lm))
    r = random.uniform(0,ts)
    n = 0
    for c in lm:
        n = n + boostedScore(c, userCountry, factor)
        if n>r and (type!='fax' or (not c.get('fax_optout', False) and c.get('fax_bxl',None))):
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
            return "This MEP is not %s"%(ms if ms else " available with this contact method")
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
        m = weighted_choice(get_filter(web.input()),'fax')
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

class Fax_personal:
    """ Handle the Fax Widget """
    def GET(self):
        """ display the fax widget """
        web.header("Content-Type", "text/html;charset=utf-8")
        template = tc.get("fax-personal.tmpl")
        wi = web.input()
        m = weighted_choice(get_filter(wi),'fax')
        if not m:
            return create_error(wi)
        if hasattr(wi,'language'):
            m['language'] = wi.language
        else:
            m['language'] = 'en';
        return template.render(m)
    def POST(self):
        "send out the fax"
        args=decode_args(web.data())
        m = get_mep_by_id(args['id'])
        if settings.TEST:
            fax = '100'
        else:
            fax = m[settings.FAX_FIELD].replace(" ","").replace("+","00")
        if args['blackhole'] != 'true':
            db.query(u"""INSERT INTO faxes (message, faxnr, create_date, campaign_id) 
                VALUES ($m,$f,$d,$s)""",
                    vars = {
                    "m" : textwrap.fill(args['full_message'],replace_whitespace=False),
                    "f" : fax,
                    "d" : datetime.datetime.now(),
                    's' : settings.campaign_id})
        template = tc.get("fax-sent.tmpl")
        web.header("Content-Type", "text/html;charset=utf-8")
        return template.render(m)

class choose_mep:
    """ Choose mep via AJAX request """
    def GET(self):
        web.header("Content-Type","application/javascript;charset=utf-8")
        web.header("Access-Control-Allow-Origin", "*")
        wi = web.input()
        m = weighted_choice(get_filter(web.input()),'fax')
        if not m:
            return """{status: 'error',message: '%s'}"""%(create_error(web.input()))
        return json.dumps(m)
        #return """{status: 'success',id: '%s',name: '%s'}"""%(m['id'],m['name'])

class Tweet:
    def GET(self):
        """display the tweet widget"""
        ff = get_filter(web.input())
        web.header("Content-Type","text/html;charset=utf-8")
        template = tc.get("tweet.tmpl")
        m = weighted_choice(lambda x: x.get('twitter',None) and ff(x), 'tweet')
        if not m:
            return create_error(web.input(),"using Twitter")
        return template.render(m)

class Subscribe:
    def GET(self):
        """subscribe to newsletter"""
        web.header("Content-Type","application/javascript;charset=utf-8")
        web.header("Access-Control-Allow-Origin", "*")
        wi = web.input()
        if hasattr(wi,'mail'):
            mail = wi.mail;
        else:
            return """{status: 'error',
                     message: 'no mail'}"""
        if hasattr(wi,'country'):
            country = wi.country
        else:
            country = ""
        logger.log(db,mail,country)
        return """{status: 'success',
                   message: 'logged mail %s from country %s'
                   }"""%(mail,country)


class mail_personal:
    """ Handle Requests for Mail """
    def GET(self):
        """ Handle GET Requests """
        web.header("Content-Type", "text/html;charset=utf-8")
        template = tc.get("mail-personal.tmpl")
        m = weighted_choice(get_filter(web.input()), 'mail')
        if not m:
            return create_error(web.input())
        return template.render(m)

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
        '/' + settings.campaign_path + '/mail_personal/', 'mail_personal',
        '/' + settings.campaign_path + '/fax/', 'Fax',
        '/' + settings.campaign_path + '/fax_personal/', 'Fax_personal',
        '/' + settings.campaign_path + '/subscribe/', Subscribe,
        '/' + settings.campaign_path + '/choose_mep/', choose_mep,
        '/' + settings.campaign_path + '/tweet/','Tweet',)

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

