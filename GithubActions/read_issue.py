'''
      - name: Write the issue to a file
        run: python read_issue.py 
        working-directory: .github/workflows/

'''
import json
import os
import sys

def get_issue_fields():
    try:
        # Get the path to the GitHub event payload file
        event_path = os.getenv('GITHUB_EVENT_PATH')

        # Read the contents of the event payload file
        with open(event_path, 'r') as file:
            event_data = json.load(file)
            # Extract the entire .issue object
            issue_fields = event_data.get('issue', {})
            return issue_fields
    except Exception as e:
        print(f"Error: {e}")
        return None

def write_to_file(data, filename):
    try:
        # Write data to the specified file in JSON format
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Issue fields written to {filename}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    issue_fields = get_issue_fields()
    if issue_fields:
        # Specify the filename where you want to write the issue fields as JSON
        # written files should not be in workflow rep. 
        # saves this to .git 
        filename = "../issue_fields.json"
        write_to_file(issue_fields, filename)
    else:
        print("Failed to retrieve issue fields.")
