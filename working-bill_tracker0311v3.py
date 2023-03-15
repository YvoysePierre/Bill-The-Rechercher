# %%
#%%
import tkinter as tk
import sys
import urllib.request
import json
import csv


def main():
    state = input("WA: ")
    bills = retrieve_state_bills(WA)
    print(f"Bills for WA:")
    for bill in bills:
        print(bill)

    # Run main loop
    while True:
        try:
            root.update_idletasks()
            root.update()
        except tk.TclError:
            break

def retrieve_state_bills(WA):
    url = f'https://api.legiscan.com/?key=ddac7961c52b60e13aeba110f6532bc3&op=getBill&id=1735313=ddac7961c52b60e13aeba110f6532bc3&op=getMasterList&state=WA'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode())
    bills = []
    for bill in data[""]:
        bill_details_url = f'https://api.legiscan.com/?key=ddac7961c52b60e13aeba110f6532bc3&op=getBillText&id=2739274=ddac7961c52b60e13aeba110f6532bc3&op=getBill&id=bill[bill_id'
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
with open('data', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    print(response)

    # Write each row to the CSV file
    for item in data:
        writer.writerow(urllib.request.urlopen(url))
        writer = csv.writer(csv_file)
#%%
