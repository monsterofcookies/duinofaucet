from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import time
from datetime import datetime, timedelta
from DailyClaim import *
from normalClaim import *
from userChecker import *
from rateLimiter import *
from viewcounter import *
from cronjob import *

# Create a FastAPI instance
app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing)
# This middleware allows requests from all origins, methods, and headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Adjust this to allow requests from specific origins
    allow_credentials=True,        # Whether or not to allow credentials (e.g., cookies) in requests
    allow_methods=["POST"],        # Methods allowed for CORS requests
    allow_headers=["*"],           # Headers allowed for CORS requests
)


# Route to handle form submission
@app.post('/24Claim')
async def dailyClaimHandler(request: Request, username: str = Form(...)):
    clientIp = request.client.host
    # Print the submitted name (for debugging)
    print(username)
    print(clientIp)
    if not isBanned(clientIp):
        #return {'message': f'I am having some issues with my faucet account ip not being able to send payments please be patient while i resolve this issue.'}
        createDatabase()
        # createRateLimitDatabase()
        # rateResult = rateCheck(clientIp)
        print(claimCheck(username,clientIp))
        claimed = claimCheck(username,clientIp)
        if claimed == False:
            if not userExists(username):
                return {'message': f'The provided user doesn\'t exist. Username: {username}'}
            else:
                dailyClaim(username)
                # The main code for sending a claim message 
                latestClaim(username, clientIp)
                return {'message': f'Successfully claimed by {username}'}

        else:
            return {'message': f'Please comeback in 24 hours to clam your ducos'}
    else:
        return isBanned(clientIp)
    # Return a response message indicating successful form submission
    # return {'message': f'Form submitted successfully! Thanks for submitting the form {username}'}
    

@app.post('/15Claim')
async def minuteClaimHandler(request: Request, username: str = Form(...)):
    clientIp = request.client.host
    print(username)
    print(clientIp)
    if not isBanned(clientIp):
        createNormalDatabase()
        claimed = normalClaimCheck(username, clientIp)
        if not claimed:
            if not userExists(username):
                return {'message': f'The provided user doesn\'t exist. Username: {username}'}
            else:
                normalClaim(username)
                normalLatestClaim(username, clientIp)
                return {'message': f'Successfully claimed by {username}'}

        else:
            return {'message': f'Please comeback in 15 minutes to claim your ducos'}
    else:
        return {'message': 'Your IP is banned from making claims'}




#taking in signups
def appendToFile(filename, content):
    with open(filename, "a") as file:
        file.write(content + "\n")

def signupCheck(username):
    with open("signups.txt", "r") as file:
        for line in file:
            if line.strip() == username:
                return True
    return False

#I closed the signups 
@app.post('/signup')
async def signup(request: Request,username: str = Form(...)):
    clientIp = request.client.host
    if not isBanned(clientIp):
        if not userExists(username):
            return {'message': f'The provided user doesn\'t exist. Username: {username}'}
        else:
            if signupCheck(username):
                return {'message': f'Sorry signups has been disabled. Please contact @_monsterofcookies on discord for allowance.'}
                # return {'message': f'The provided user has already been added to the list. Username: {username}'}
            else:
                appendToFile("signups.txt", username)
                return {'message': f'Sorry signups has been disabled. Please contact @_monsterofcookies on discord for allowance.'}
                # return {'message': f'The provided user has been added to the list. Username: {username}'}
    else:
        return isBanned(clientIp)



@app.post('/view')
async def count(request: Request):
    clientIp = request.client.host
    if not isBanned(clientIp):
        if addToTodayViews(clientIp):
            print("Couted a vivew")
        else:
            print("did not count a vivew as the vivew is already counted")
    else:
        return isBanned(clientIp)

def getData():
    connection = sqlite3.connect("siteStats.db")
    cursor = connection.cursor()
    cursor.execute("SELECT date, views, balance FROM stats ORDER BY date")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows



#Gets and formats the data from the DB so chart.js can render it
@app.get("/stats")
def stats(request: Request):
    clientIp = request.client.host
    if not isBanned(clientIp):
        data = getData()
        formattedData = {
            "dates": [row[0] for row in data],
            "views": [row[1] for row in data],
            "balances": [row[2] for row in data]
        }
        return formattedData
    else:
        return isBanned(clientIp)
    
"""
This is the part that handles the addiiton of the data in the database. 
This part is ran by a remote server with a get request. 
You can run the code from local cron job in linux.

"""


@app.get('/cron')
async def cronjob(request: Request):
    clientIp = request.client.host
    if not isBanned(clientIp):
        cron()
        return {'message': 'croned'}
    else:
        return isBanned(clientIp)