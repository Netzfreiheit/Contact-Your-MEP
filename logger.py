import settings
import databaseconnect
import datetime

def log(db,action,value=""):
    db.query(u"""INSERT INTO logs (action,value,date) VALUES ($action,$value,$date)""",
        vars = {"action" : action,
                  "value" : value,
                  "date" : datetime.datetime.now()})
