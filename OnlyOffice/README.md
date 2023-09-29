# OnlyOffice API Scripts

This project contains Python scripts for interacting with the OnlyOffice API.

## Overview

The scripts allow you to:

- Get an API token
- Retrieve users and groups
- Create, update, and manage users
- Add/remove users from groups

## Files

**extract_token.py**

Gets an API token by authenticating with username and password.

**get_all.py** 

Retrieves all users and/or groups from OnlyOffice.

**people_and_groups.py**

Creates, updates, and manages OnlyOffice users and groups:

- Create new users
- Update existing users
- Get user ID from email
- Add/remove users from groups

**README.md**

This readme providing an overview of the project.

## Usage

1. Run `extract_token.py` to get an API token
2. Set the `ONLY_OFFICE_API_TOKEN` environment variable 
3. Import and use the functions from `get_all.py` and `people_and_groups.py`

See docstrings and comments in each file for more details.

## Requirements

- Python 3
- requests
- OnlyOffice account credentials
