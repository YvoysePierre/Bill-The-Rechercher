
import json
import csv

# Open the JSON file and read its contents
with open("C:\\Users\\ManisPierre\\DataspellProjects\\Bill_autogui0311\\Bill-The-Rechercher\\Untitled-2.json") as json_file:
    json_text = json_file.read()

# Parse the JSON data into a Python object
data = json.loads(json_text)

# Open a new CSV file for writing
with open('output.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Write each row to the CSV file
    for item in data:
        row = [str(value) for value in item.values()]
        writer.writerow(row)

#%%
