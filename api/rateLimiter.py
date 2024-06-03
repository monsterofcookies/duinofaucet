from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import sqlite3

app = FastAPI()
def iniDatabase():
# Initialize databases
    grayListDb = sqlite3.connect("grayList.db")
    blackListDb = sqlite3.connect("blackList.db")

    # Create tables if not exists
    grayListDb.execute("CREATE TABLE IF NOT EXISTS ips (ip TEXT PRIMARY KEY)")
    blackListDb.execute("CREATE TABLE IF NOT EXISTS ips (ip TEXT PRIMARY KEY)")

requestCounts = {}
rateLimit = 8  # Number of requests allowed per 20 seconds
rateLimitPeriod = timedelta(seconds=20)  # Time period for rate limiting


# Function to check rate limit
def checkRateLimit(ipAddress):
    if ipAddress not in requestCounts:
        requestCounts[ipAddress] = {"timestamp": datetime.now(), "count": 0}
    else:
        currentTime = datetime.now()
        if currentTime - requestCounts[ipAddress]["timestamp"] > rateLimitPeriod:
            requestCounts[ipAddress] = {"timestamp": currentTime, "count": 0}
    requestCounts[ipAddress]["count"] += 1
    return requestCounts[ipAddress]["count"] > rateLimit


# Function to add IP to graylist
def addToGrayList(ipAddress):
    try:
        iniDatabase()
        grayListDb = sqlite3.connect("grayList.db")
        grayListDb.execute("INSERT INTO ips (ip) VALUES (?)", (ipAddress,))
        grayListDb.commit()
        print(f"IP {ipAddress} added to graylist.")
        return True
    except sqlite3.IntegrityError:
        print(f"IP {ipAddress} already exists in graylist.")
        return False


# Function to add IP to blacklist
def addToBlackList(ipAddress):
    try:
        iniDatabase()
        blackListDb = sqlite3.connect("blackList.db")
        blackListDb.execute("INSERT INTO ips (ip) VALUES (?)", (ipAddress,))
        blackListDb.commit()
        print(f"IP {ipAddress} added to blacklist.")
        return True
    except sqlite3.IntegrityError:
        print(f"IP {ipAddress} already exists in blacklist.")
        return False



def isBanned(ip):
    if checkRateLimit(ip):
        if not addToBlackList(ip):
            raise HTTPException(status_code=403, detail="Rate limit exceeded. You were warned previously and now, banned!")
        elif not addToGrayList(ip):
            addToBlackList(ip)
            raise HTTPException(status_code=403, detail="Rate limit exceeded. Please try again later. You were warned previously and now have been added to the blacklist!")
        else:
            addToGrayList(ip)
            raise HTTPException(status_code=403, detail="Rate limit exceeded. Please try again later. You are warned and now have been added to the graylist!")
    else:
        return False


#this one is basically useless
# Function to check and manage IPs based on warning counts
# def checkAndManageIp(ipAddress):
#     iniDatabase()
#     if ipAddress in requestCounts and requestCounts[ipAddress]["count"] >= rateLimit:
#         # Check if IP is already in blacklist, if not, add it
#         cursor = blackListDb.execute("SELECT * FROM ips WHERE ip=?", (ipAddress,))
#         if cursor.fetchone() is not None:
#             return {'message': "IP is in blacklist. Access forbidden."}

#         # If IP is already in blacklist, check graylist
#         cursor = grayListDb.execute("SELECT * FROM ips WHERE ip=?", (ipAddress,))
#         if cursor.fetchone() is not None:
#             return {'message': "IP is in graylist. Access forbidden."}

#         addToBlackList(ipAddress)
#         return {'message': "IP added to blacklist. Access forbidden."}
    
#     return {}




