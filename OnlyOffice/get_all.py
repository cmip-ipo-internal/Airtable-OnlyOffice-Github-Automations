'''

OnlyOffice API scripts made for the CMIP-IPO
All queries: contact the IPO Technical Officer: 
Daniel Ellis
daniel.ellis -@- ext.esa.int


'''


import os
import sys
import requests
from pprint import pprint
from typing import Any, Dict, Union, List

# Retrieve the API token from the environment variable
api_token = os.environ.get("ONLY_OFFICE_API_TOKEN")

# Check if the API token is available
if api_token is None:
    print("API token is not set in the environment variable ONLY_OFFICE_API_TOKEN.")
    sys.exit(1)

PORTAL = "wcrp-cmip.onlyoffice.eu"

def get(what: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    '''
    Make a GET request to the OnlyOffice API.

    Args:
        what (str): The API endpoint to retrieve data from.

    Returns:
        Union[Dict[str, Any], List[Dict[str, Any]]]: JSON response from the API.
    '''
    # Define the API URL
    api_url = f"https://{PORTAL}/api/2.0/{what}"

    # Define the headers with the API token
    headers = {
        "Host": PORTAL,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    # Send a GET request
    response = requests.get(api_url, headers=headers)

    # Check the response status and content
    if response.status_code == 200:
        data = response.json()
        return data['response']
    else:
        print(response.text)
        response.raise_for_status()

def people() -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    '''
    Retrieve information about people from the OnlyOffice API.

    Returns:
        Union[Dict[str, Any], List[Dict[str, Any]]]: JSON response containing people data.
    '''
    return get('people')

def groups() -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    '''
    Retrieve information about groups from the OnlyOffice API.

    Returns:
        Union[Dict[str, Any], List[Dict[str, Any]]]: JSON response containing group data.
    '''
    return get('group')

def email(eaddr: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    '''
    Retrieve user information based on their email address from the OnlyOffice API.

    Args:
        eaddr (str): Email address of the user.

    Returns:
        Union[Dict[str, Any], List[Dict[str, Any]]]: JSON response containing user data.
    '''
    what = f"people/email?email={eaddr}"
    return get(what)

def whoami() -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    '''
    Retrieve information about the user whose credentials are being used from the OnlyOffice API.

    Returns:
        Union[Dict[str, Any], List[Dict[str, Any]]]: JSON response containing user data.
    '''
    return get('people/@self')

def format_json(jsn: Union[Dict[str, Any], List[Dict[str, Any]]]) -> None:
    '''
    Pretty print JSON data.

    Args:
        jsn (Union[Dict[str, Any], List[Dict[str, Any]]]): JSON data to be printed.
    '''
    pprint(jsn)

# Example usages of the functions
# if __name__ == '__main__':
#     print("People:")
#     format_json(people())
#     print("\nGroups:")
#     format_json(groups())
#     print("\nUser Information (based on email):")
#     format_json(email('example@example.com'))
#     print("\nWho Am I:")
#     format_json(whoami())
