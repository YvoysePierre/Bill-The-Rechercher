import requests

def retrieve_state_bills(state):
    # Make HTTP request to retrieve bills for specified state
    response = requests.get(f'https://api.govinfo.gov/collections/BILLS/{state}/?offset=0&pageSize=kazR3nvKu68LDqQ7KPU5bNKp2mPD4pHS9MsAHEOa')
    response_data = response.json()

    # Extract bill names from JSON response and add to list
    bills = []
    for result in response_data['packages']:
        bills.append(result['title'])

    # Return list of bills
    return bills
