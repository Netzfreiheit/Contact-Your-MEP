import urlparse
import web

def connect(url):
    r = urlparse.urlparse(url)
    if r.scheme == 'sqlite':
        if (r.path != ''):
            db = r.path
        else:
            db = r.netloc
        return web.database(dbn='sqlite', db=db)
    if r.scheme == 'mysql':
        return web.database(dbn='mysql',
                host = r.hostname,
                user = r.username,
                pw = r.password,
                db = r.path[1:])

