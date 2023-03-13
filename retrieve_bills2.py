import requests

def retrieve_state_bills(state):
    api_key = "YOUR_API_KEY_HERE" # Replace with your API key
    url = f"https://v3.openstates.org/bills/ocd-bill/%7Bopenstates_bill_id%7D={WA}&apikey={a9c90f282ff24dc79b08d23ffcaf5e7a}"
    response = requests.get(url)

    # Check if API request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve bills for {state}. Status code: {response.status_code}")

    # Extract bill titles from JSON response and add to list
    bills = []
    results = response.json()
    for result in results:
        title = result["title"]
        bills.append(title)

    # Return list of bills
    return bills
#%%
