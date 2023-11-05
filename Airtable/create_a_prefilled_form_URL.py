'''
Author and Maintainer contact 
  daniel.ellis (at) ext.esa.int
'''

def generate_airtable_form_url(base_id, table_name, fields):
    """
    Generates a pre-filled Airtable form URL with the given base ID, table name, and pre-fill fields.

    Args:
        base_id (str): The unique identifier of the Airtable base.
        table_name (str): The name of the Airtable table.
        fields (dict): A dictionary containing pre-fill field names as keys and corresponding values.

    Returns:
        str: The pre-filled Airtable form URL.

    Example:
        >>> base_id = 'xxxxxxxxxxx'
        >>> table_name = 'yyyyyyyyyy'
        >>> fields = {
        ...     'Name': 'York',
        ...     'ROR': 'https://ror.org/04m01e293',
        ...     'Assignee': 'Dan'
        ... }
        >>> generate_airtable_form_url(base_id, table_name, fields)
        'https://airtable.com/appaZflpqbFjA6pwV/shrNALXGlKZAk76iD?prefill_Name=York&prefill_ROR=https://ror.org/04m01e293&prefill_Assignee=dan'
    """
    base_url = f'https://airtable.com/{base_id}/{table_name}'
    # Construct the URL parameters for pre-filling the form fields
    params = "&".join([f'prefill_{key}={value}' for key, value in fields.items()])
    airtable_form_url = f'{base_url}?{params}'
    return airtable_form_url

# Example usage
if __name__ == "__main__":
    # Replace the following values with your actual base ID, table name, and pre-fill fields
    
    #  table / form information
    base_id = 'xxxxxxxxxxx'
    table_name = 'yyyyyyyyyy'

    #  A dictionary containing the field name -> value  of those which we want to prefill. 
    #  an example is given below
    fields = {
        'Name': 'York',
        'ROR': 'https://ror.org/04m01e293',
        'Assignee': 'Dan'
    }

    # Generate the pre-filled Airtable form URL
    
    airtable_form_url = generate_airtable_form_url(base_id, table_name, fields)
    
    print(f'Pre-filled Airtable form URL: {airtable_form_url}')
