import sqlite3
import time
from dotenv import load_dotenv
import os
import requests as rq



allowedTime = 24*60*60
def createDatabase():
    # Connect to the database (or create it if it doesn't exist)
    con = sqlite3.connect('DailyClaims.db')
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



def claimCheck(username, ip):
    con = sqlite3.connect("DailyClaims.db")
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

    if timeDiff > (allowedTime):
        print("The user has not claimed today")
        return False
    else: 
        print("The user has claimed today")
        return True

    

def latestClaim(username, ip):
    # Connect to the database
    con = sqlite3.connect("DailyClaims.db")
    cur = con.cursor()

    # Get the current timestamp
    claimTime = int(time.time())

    # Execute an INSERT query to insert the new claim
    cur.execute("INSERT INTO Claims (username, ip, time) VALUES (?, ?, ?)", (username, ip, claimTime))

    # Commit the transaction
    con.commit()

    # Close the database connection
    con.close()


def dailyClaim(username):
    load_dotenv()

    #change this for chaning the faucet payout
    amount = 5
    Uname = os.getenv('UNAME')
    Pass = os.getenv('PASS')
    print(rq.get(f'https://server.duinocoin.com/transaction?username={Uname}&password={Pass}&recipient={username}&amount={amount}&memo=Claim%20at:https://duinofaucet.onrender.com').text)
