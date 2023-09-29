'''
A script to get the OnlyOffice API token


OnlyOffice API scripts made for the CMIP-IPO
All queries: contact the IPO Technical Officer: 
Daniel Ellis
daniel.ellis -@- ext.esa.int


'''


import getpass
import requests
import json

PORTAL = "wcrp-cmip.onlyoffice.eu"

def get_onlyoffice_token(username: str, password: str) -> str:
    '''
    Authenticate user and get OnlyOffice API token.

    Args:
        username (str): OnlyOffice email address.
        password (str): OnlyOffice password.

    Returns:
        str: OnlyOffice API token if authentication is successful, otherwise an empty string.
    '''
    print(f"Portal: {PORTAL}\n")

    # Define the API URL
    api_url = f"https://{PORTAL}/api/2.0/authentication.json"

    # Create a dictionary containing the payload data
    payload = {
        "username": username,
        "password": password
    }

    # Set the headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make a POST request
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)

    # Check the response status and content
    if response.status_code == 201:
        data = response.json()['response']
        print("Authentication successful:")
        token = data.get('token')
        print(token)
        print('Add to bash_profile')
        print(f"export ONLY_OFFICE_API_TOKEN='{token}'")
        print('')

        print('---- EXPIRES -----')
        print(data.get('expires'))
        print('')
        return token
    else:
        print(f"Authentication failed with status code: {response.status_code}")
        print(response.text)
        return ''

if __name__ == '__main__':
    username = input('OnlyOffice Email: ')
    assert '@' in username
    # Prompt the user for a password without displaying the input
    password = getpass.getpass('OnlyOffice Password: ')
    get_onlyoffice_token(username, password)
