import json
import requests
from pprint import pprint

# disable https warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    # Global Variables
    auth_file    = "./session.json"
    creds       = json.load(open(auth_file))

    # Request Variables
    headers     = {}
    payload     = ""
    cookies     = "" # This variable isn't used in this script, but it may be used in other scripts to store the session token.

    # Create session
    session     = requests.Session()

    login       = {'username': creds['username'], 'password': creds['password']}
    response    = session.get(creds['url']+"api/login", params=login, headers=headers, data=payload, verify=False)

    # Check login success
    if response.status_code == 200:
        json_data = response.json()['_global_result']

        # Get session token from the _global_result
        session_token = json_data['UIDARUBA']

        # Update auth_file
        creds['token'] = session_token
        with open(auth_file, 'w') as outfile:
            json.dump(creds, outfile)
    else:
        pprint("Login failed with status code:", response.status_code)

if __name__ == "__main__":
    main()