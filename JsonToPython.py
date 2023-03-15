import json
import csv

# Open the JSON file and read its contents
with open("Untitled-2.json") as json_file:
    data = json.loads(json_file)

# Open a new CSV file for writing
with open('output.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Write the header row based on the keys in the first item
    header = list(data[0].keys())
    writer.writerow(header)

    # Write each row to the CSV file
    for item in data:
        row = [str(item.get(key, '')) for key in header]
        writer.writerow(row)


#%%
