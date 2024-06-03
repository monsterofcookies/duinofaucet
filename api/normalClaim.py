import sqlite3
import time
from dotenv import load_dotenv
import os
import requests as rq
import random

allowedTime = 15 * 60  # 15 minutes in seconds

def createNormalDatabase():
    # Connect to the database (or create it if it doesn't exist)
    con = sqlite3.connect('NormalClaims.db')
    cur = con.cursor()

    # Create a table
    cur.execute('''CREATE TABLE IF NOT EXISTS Claims (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    ip TEXT,
                    time INTEGER
                    )''')

    # Commit changes and close connection
    con.commit()
    con.close()

def normalClaimCheck(username, ip):
    con = sqlite3.connect("NormalClaims.db")
    cur = con.cursor()

    # Fetch the latest entry for the given username and IP address
    cur.execute("SELECT username, ip, time FROM Claims WHERE username = ? OR ip = ? ORDER BY time DESC LIMIT 1", (username, ip))
    latestEntry = cur.fetchone()

    # Close the connection
    con.close()

    if latestEntry is None:
        # If no entry exists for the given username and IP address, return False
        return False

    # Unpack the latest entry
    claimUsername, claimIp, latestTime = latestEntry

    # Calculate the time difference
    timeDiff = time.time() - latestTime

    print(latestTime, timeDiff)

    if timeDiff > allowedTime:
        print("The user can claim again")
        return False
    else: 
        print("The user has already claimed within the last 15 minutes")
        return True

def normalLatestClaim(username, ip):
    # Connect to the database
    con = sqlite3.connect("NormalClaims.db")
    cur = con.cursor()

    # Get the current timestamp
    claimTime = int(time.time())

    # Execute an INSERT query to insert the new claim
    cur.execute("INSERT INTO Claims (username, ip, time) VALUES (?, ?, ?)", (username, ip, claimTime))

    # Commit the transaction
    con.commit()

    # Close the database connection
    con.close()

def normalClaim(username):

    randomamt = round(random.uniform(0.01, 2), 2)

    #change this for a different message
    message = 'SOME MESSAGE'
    load_dotenv()
    Uname = os.getenv('UNAME')
    Pass = os.getenv('PASS')
    print(rq.get(f'https://server.duinocoin.com/transaction?username={Uname}&password={Pass}&recipient={username}&amount={randomamt}&memo={message}').text)
