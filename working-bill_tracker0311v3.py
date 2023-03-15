# %%
#%%
import tkinter as tk
import sys
import urllib.request
import json
import csv


def main():
    state = input("Enter a state to retrieve bills: ")
    bills = retrieve_state_bills(state)
    print(f"Bills for {state}:")
    for bill in bills:
        print(bill)

    # Run main loop
    while True:
        try:
            root.update_idletasks()
            root.update()
        except tk.TclError:
            break

def retrieve_state_bills(state):
    url = f'https://api.legiscan.com/?key=ddac7961c52b60e13aeba110f6532bc3&op=getBill&id=1735313={ddac7961c52b60e13aeba110f6532bc3}&op=getMasterList&state={State}'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode())
    bills = []
    for bill in data["masterlist"]:
        bill_details_url = f'https://api.legiscan.com/?key=ddac7961c52b60e13aeba110f6532bc3&op=getBillText&id=2739274={ddac7961c52b60e13aeba110f6532bc3}&op=getBill&id={bill[bill_id]}'
        bill_details_response: object = urllib.request.urlopen(bill_details_url)
        bill_details_data = json.loads(bill_details_response.read().decode())
        bill_dict = {{
            "title": bill["title"],
            "description": bill_details_data["bill"]["description"],
            "summary": bill_details_data["bill"]["summary"],
            "link": f"https://legiscan.com/{state}/bill/{bill['bill_number']}"
        }},
        bills.append(bill_dict)
    return bills


API_KEY = "ddac7961c52b60e13aeba110f6532bc3"
state = "WA"
url = f"https://api.legiscan.com/?key=ddac7961c52b60e13aeba110f6532bc3&op=getMasterList&state=WA"
response: object = urllib.request.urlopen(url)
data = json.loads(response.read().decode())
print(data)

# Open a new CSV file for writing
with open('output.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

# Write the header row based on the keys in the first item
header = list(data[0].keys())
writer.writerow(header)

for item in data:
    row = [str(item.get(key, '')) for key in header]
    writer.writerow(row)
#%%
