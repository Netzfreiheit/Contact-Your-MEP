import settings
import databaseconnect
import datetime

def log(action,value=""):
    sql = databaseconnect.connect(settings.DATABASE_URL)
    cur = sql.cursor()
    cur.execute(databaseconnect.convert("""INSERT INTO logs (action,value,date) VALUES (?,?,?)"""),
        (action,value,datetime.datetime.now().isoformat()));
    sql.commit()
