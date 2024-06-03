import sqlite3
import requests as rq
from datetime import datetime
import json

def countViews():
    # Get the current UTC date and time
    currentUtcDateTime = datetime.utcnow()

    # Extract the date part and format it as a string (e.g., 'YYYY-MM-DD')
    currentUtcDate = currentUtcDateTime.strftime('%Y-%m-%d')

    print("Current UTC date:", currentUtcDate)

    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect('todayViews.db')

    # Create a cursor object
    cursor = connection.cursor()

    # Execute the COUNT query
    cursor.execute("SELECT COUNT(*) FROM ip")

    # Fetch the result
    count = cursor.fetchone()[0]

    # Print the count
    print(f"Total number of items in the table: {count}")

    # Close the cursor and connection
    cursor.close()
    connection.close()

    response = rq.get('https://server.duinocoin.com/balances/_monsterofcookies').text
    responseJson = json.loads(response)

    balance = responseJson['result']['balance']
    print('Wallet balance: ', balance)

    return currentUtcDate, count, balance

def addToStats(date, count, balance):
    siteStats = sqlite3.connect("siteStats.db")
    siteStats.execute("CREATE TABLE IF NOT EXISTS stats (date TEXT PRIMARY KEY, views INTEGER, balance FLOAT)")

    siteStats.execute("""
        INSERT INTO stats (date, views, balance)
        VALUES (?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            views = views + excluded.views,
            balance = excluded.balance
    """, (date, count, balance))
    
    # Commit the changes
    siteStats.commit()
    
    # Close the connection
    siteStats.close()

def clearTodayViews():
    connection = sqlite3.connect('todayViews.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ip")
    connection.commit()
    cursor.close()
    connection.close()

def cron():
    # Count views and get date, count, and balance
    date, count, balance = countViews()
    
    # Add data to site stats
    addToStats(date, count, balance)

    # Clear todayViews
    clearTodayViews()

