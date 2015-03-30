import settings
import databaseconnect
import datetime

def log(db,mail,country=""):
    db.query(u"""INSERT INTO subscriptions (mail,country,create_date) VALUES ($mail,$country,$create_date)""",
        vars = {"mail" : mail,
                  "country" : country,
                  "create_date" : datetime.datetime.now()})
