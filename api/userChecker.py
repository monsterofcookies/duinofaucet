import requests as rq
import json

url = 'https://server.duinocoin.com/users/'

def userExists(username):
    try:
        response = rq.get(url + username)
        if response.status_code == 200:
            responseJson = json.loads(response.text)
            # print(responseJson)
            message = responseJson.get("message")
            if message and "This user doesn't exist" in message:
                return False  # User doesn't exist
            else:
                return True   # User exists
        else:
            return f"Error: Status Code {response.status_code}"
    except rq.RequestException as e:
        return f"Error: {e}"

# username = '_monsterofcookies'
# if userExists(username):
#     print(f"User '{username}' exists.")
# else:
#     print(f"User '{username}' doesn't exist.")
