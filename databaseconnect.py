import urlparse

def connect(url):
    r = urlparse.urlparse(url)
    if r.scheme == 'sqlite':
        import sqlite3
        return sqlite3.connect(r.netloc)
    if r.scheme == 'mysql':
        import MySQLdb
        return MySQLdb.connect(host = r.hostname,
                user = r.username,
                passwd = r.password,
                db = r.path[1:])

def convert(query):
    import settings
    r = urlparse.urlparse(settings.DATABASE_URL)
    if r.scheme = 'sqlite':
        return query
    if r.scheme = 'mysql':
        return query.replace("?","%s")
