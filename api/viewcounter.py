from datetime import datetime, timedelta
import sqlite3

def iniDatabase():
    siteStats = sqlite3.connect("siteStats.db")
    todayViews = sqlite3.connect("todayViews.db")

    siteStats.execute("CREATE TABLE IF NOT EXISTS stats (date DATE TEXT PRIMARY KEY, views INTEGER, balance FLOAT )")
    todayViews.execute("CREATE TABLE IF NOT EXISTS ip (ip TEXT PRIMARY KEY)")


def addToTodayViews(ipAddress):
    try:
        iniDatabase()
        todayViews = sqlite3.connect("todayViews.db")
        todayViews.execute("INSERT INTO ip (ip) VALUES (?)", (ipAddress,))
        todayViews.commit()
        print(f"IP {ipAddress} added to todayViews.")
        return True
    except sqlite3.IntegrityError:
        print(f"IP {ipAddress} already exists in todayViews.")
        return False
