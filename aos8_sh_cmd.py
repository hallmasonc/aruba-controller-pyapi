import aos8_init_session
import aos8_logout_session
import csv
import json
import requests
import time
from pprint import pprint

# disable https warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global Variables
auth_file   = "./session.json"
creds       = {}

def read_auth(file):
    return json.load(open(file))

def sh_cmd(command):
    # Load auth_file
    creds = read_auth(auth_file)

    # Check auth_file for token value
    if creds['token'] == "(null)":
        aos8_init_session.main()
        creds = read_auth(auth_file)

    # Request Variables
    headers     = {
        'Content-Type'  : 'application/json',
        'Accept'        : 'application/json',
        'Cookie'        : f'SESSION={creds['token']}'
    }
    payload     = ""

    # Request Parameters
    sh_params   = {
        'command'   : 'show ' + command,
        'UIDARUBA'  : creds['token']
    }

    # Create session
    session     = requests.Session()
    response    = session.get(creds['url']+"configuration/showcommand", params=sh_params, headers=headers, data=payload, verify=False)
    return response.json()

def main():
    # Variables
    output_file = "./ap_database.csv"

    # Get access point database
    apdb = sh_cmd('ap database long')

    # Create output .csv
    with open(output_file, 'w') as csv_file:
        write   = csv.writer(csv_file)

        # Get data headers
        fields  = apdb['_meta']

        # Iterate through database
        for ap in apdb["AP Database"]:
            # Create the rows to be output
            data_row = []

            # Create the column headers
            for f in fields:
                data_row.append(ap[f])

            # Append the data_row to the .csv file
            write.writerow(data_row)
    
    # Logout
    aos8_logout_session.main()

if __name__ == "__main__":
    main()