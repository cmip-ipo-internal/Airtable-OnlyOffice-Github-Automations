'''

OnlyOffice API scripts made for the CMIP-IPO
All queries: contact the IPO Technical Officer: 
Daniel Ellis
daniel.ellis -@- ext.esa.int


'''

import os
import sys
import re
import requests
from pprint import pprint
from typing import List, Union, Dict, Any

# Retrieve the API token from the environment variable
api_token = os.environ.get("ONLY_OFFICE_API_TOKEN")

# Check if the API token is available
if api_token is None:
    print("API token is not set in the environment variable ONLY_OFFICE_API_TOKEN.")
    sys.exit(1)

PORTAL = "wcrp-cmip.onlyoffice.eu"

###################################
### Requests
###################################

def get(payload: Dict[str, Any], what: str = 'people', checks: bool = True, kind: str = 'POST') -> Dict[str, Any]:
    '''
    Make a POST, PUT, or DELETE request to the OnlyOffice API.

    Args:
        payload (Dict[str, Any]): JSON payload data to be sent with the request.
        what (str): The API endpoint to send the request to.
        checks (bool): Perform data validation checks if True. Default is True.
        kind (str): Type of request ('POST', 'PUT', or 'DELETE'). Default is 'POST'.

    Returns:
        Dict[str, Any]: JSON response from the API.
    '''
    global PORTAL

    # Define the API URL
    api_url = f"https://{PORTAL}/api/2.0/{what}"

    # Define the headers with the API token
    headers = {
        "Host": PORTAL,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    if checks:
        payload['firstname'] = re.sub(r'[^a-zA-Z]', '', payload['firstname'])
        payload['lastname'] = re.sub(r'[^a-zA-Z]', '', payload['lastname'])

    # Create a session
    session = requests.Session()
    # Set headers
    session.headers.update(headers)

    # Send the request using the session
    if kind == 'POST':
        response = session.post(api_url, json=payload)
    elif kind == 'PUT':
        response = session.put(api_url, json=payload)
    elif kind == 'DELETE':
        response = session.delete(api_url, json=payload)
    else:
        raise KeyError(f"{kind} is not a valid session command.")

    # Check the response status and content
    if response.status_code not in [200, 201, 500, 403]:
        raise NotImplementedError(f'The URL ({api_url}) returned no response. {response.json()} ')

    return response.json()

###################################
### User Tools
###################################

def add_user(values: Dict[str, Any], payload: Dict[str, Any] = None) -> Dict[str, Any]:
    '''
    Add a new user to OnlyOffice.

    Args:
        values (Dict[str, Any]): Dictionary containing user information.
        payload (Dict[str, Any]): JSON payload data. Default is None.

    Returns:
        Dict[str, Any]: JSON response from the API.
    '''
    assert 'firstname' in values
    assert 'lastname' in values
    assert 'email' in values

    payload = payload or {
        "isVisitor": 'False',
        "email": values['email'],
        "firstname": values['firstname'],
        "lastname": values['lastname'],
        "title": values['title'],
        "location": "some text",
        "password": values['password'],
        'isAdmin': False,
        'isLDAP': False,
        'isOwner': False,
        'isSSO': False,
    }

    response = get(payload)

    if response.status_code == 201:
        data = response.json()
        print("GET Request Successful:")
        pprint(data)
        return data['response']
    elif response.status_code == 500:
        try:
            if response["error"]["message"] == "Member with this email is already registered":
                print('--- updating existing user ---')
                data = update_user(values['email'], payload)
                pprint(data)
                return data['response']
        except:
            print(response.text)
            print(f"GET Request Failed with status code: {response.status_code}")

    return {}


def update_user(email: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Update user information in OnlyOffice.

    Args:
        email (str): Email of the user to be updated.
        payload (Dict[str, Any]): JSON payload data.

    Returns:
        Dict[str, Any]: JSON response from the API.
    '''
    uid = get_all.email(email).get('id')
    assert uid
    what = f'people/{uid}'
    response = get(payload, what=what, checks=False, kind='PUT')

    output = response.json()
    return output

###################################
### Group Tools
###################################


def add_group_members(group: str, member_emails: List[str]) -> None:
    '''
    Add members to a group in OnlyOffice.

    Args:
        group (str): Group name.
        member_emails (List[str]): List of member emails to be added to the group.

    Returns:
        None
    '''
    members = [get_all.email(email).get('id') for email in member_emails]
    what = f'group/{group}/members'
    payload = {"members": members}
    response = get(payload, what=what, checks=False, kind='PUT')

    print('Group members updated.')
    pprint(response.json())


def rm_group_members(group: str, member_emails: List[str]) -> None:
    '''
    Remove members from a group in OnlyOffice.

    Args:
        group (str): Group name.
        member_emails (List[str]): List of member emails to be removed from the group.

    Returns:
        None
    '''
    members = [get_all.email(email).get('id') for email in member_emails]
    what = f'group/{group}/members'
    payload = {"members": members}
    response = get(payload, what=what, checks=False, kind='DELETE')

    print('Group members updated.')
    pprint(response.json())
