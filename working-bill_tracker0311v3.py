import tkinter as tk
import sqlite3
import csv
import sys
import string
import requests
import urllib.request
import json
import urllib.request
from tkinter import filedialog, messagebox, simpledialog, Menu


# Define function for main app window
def main():
    # Create main window
    global root
    root = tk.Tk()
    root.title("Bills Tracker")
    root.geometry("800x600")

    # Define GUI components
    title_label = tk.Label(root, text="Bills Tracker", font=("Arial", 24))
    title_label.pack(pady=20)
    menu_bar: Menu = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Export Bills", command=export_bills_gui)
    file_menu.add_command(label="Import Bills", command=import_bills_gui)
    menu_bar.add_cascade(label="File", menu=file_menu)
    search_button = tk.Button(root, text="Search Bills", font=("Arial", 16), command=search_bills_gui)
    search_button.pack(pady=20)
    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    global listbox
    listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    # Load bills into listbox
    load_bills()

    # Set menu bar and run main loop
    root.config(menu=menu_bar)
    root.mainloop()


# Define function to load bills into listbox
def load_bills():
    # Clear existing bills in listbox
    listbox.delete(0, tk.END)

    # Load bills from database and insert into listbox
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bills")
    bills = c.fetchall()
    for bill in bills:
        listbox.insert(tk.END, bill[1])
    conn.close()


# Define function to add a new bill
def add_bill():
    # Prompt user for bill details
    title = simpledialog.askstring("New Bill", "Enter bill title:")
    description = simpledialog.askstring("New Bill", "Enter bill description:")
    category = simpledialog.askstring("New Bill", "Enter bill category:")
    state = simpledialog.askstring("New Bill", "Enter state bill is in:")
    introduced = simpledialog.askstring("New Bill", "Enter date bill was introduced (YYYY-MM-DD):")
    status = simpledialog.askstring("New Bill", "Enter bill status:")
    link = simpledialog.askstring("New Bill", "Enter bill link:")

    # Add new bill to database and listbox
    if title and introduced:
        conn = sqlite3.connect('bills.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO bills (title, description, category, state, introduced, status, link) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (title, description, category, state, introduced, status, link))
        conn.commit()
        conn.close()
        listbox.insert(tk.END, title)
        messagebox.showinfo("New Bill", "Bill added successfully.")


# Define function to export bills to CSV file
def export_bills():
    # Prompt user for file name and location
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        # Export bills to CSV file
        conn = sqlite3.connect('bills.db')
        c = conn.cursor()
        c.execute("SELECT * FROM bills")
        bills = c.fetchall()
        with open(file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Title", "Description", "Category", "State", "Introduced", "Status", "Link"])
            for bill in bills:
                writer.writerow(bill[1:])
        conn.close()
        messagebox.showinfo("Export Bills", "Bills exported successfully.")


# Define the function for deleting bills
# Define function to delete bill
def delete_bill():
    # Get selected bill from listbox
    selection = listbox.curselection()
    if selection:
        # Prompt user to confirm deletion
        if messagebox.askyesno("Delete Bill", "Are you sure you want to delete this bill?"):
            # Delete bill from database and listbox
            conn = sqlite3.connect('bills.db')
            c = conn.cursor()
            title = listbox.get(selection[0])
            c.execute("DELETE FROM bills WHERE title=?", (title,))
            conn.commit()
            conn.close()
            listbox.delete(selection[0])
            messagebox.showinfo("Delete Bill", "Bill deleted successfully.")
    else:
        messagebox.showerror("Delete Bill", "Please select a bill to delete.")

        # Define main function


def main():
    state = input("Enter a state to retrieve bills: ")
    bills = retrieve_state_bills(state)
    print(f"Bills for {state}:")
    for bill in bills:
        print(bill)

    # Create main window
    root = tk.Tk()
    root.title("Bill Tracker")
    root.geometry("800x600")

    # Create listbox for displaying bills
    listbox = tk.Listbox(root, width=80)
    listbox.pack(padx=20, pady=20)

    # Create scrollbar for listbox
    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # Create frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(padx=20, pady=10)

    # Create buttons
    add_button = tk.Button(button_frame, text="Add Bill", command=add_bill)
    add_button.pack(side=tk.LEFT, padx=5)
    edit_button = tk.Button(button_frame, text="Edit Bill", command=edit_bill)
    edit_button.pack(side=tk.LEFT, padx=5)
    delete_button = tk.Button(button_frame, text="Delete Bill", command=delete_bill)
    delete_button.pack(side=tk.LEFT, padx=5)
    export_button = tk.Button(button_frame, text="Export Bills", command=export_bills)
    export_button.pack(side=tk.LEFT, padx=5)
    import_button = tk.Button(button_frame, text="Import Bills", command=import_bills)
    import_button.pack(side=tk.LEFT, padx=5)
    search_button = tk.Button(button_frame, text="Search Bills", command=search_bills)
    search_button.pack(side=tk.LEFT, padx=5)

    # Populate listbox with bills from database
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bills")
    bills = c.fetchall()
    for bill in bills:
        listbox.insert

    # Run main loop

    # Run main loop
    while True:
        try:
            root.update_idletasks()
            root.update()
        except tk.TclError:
            break


# This function creates the main window and sets up the listbox and buttons. It also populates the listbox with bills
# from the database. The main loop runs the user interface and waits for user input.

# Finally, call the main function to start the program:
# Call main function
def retrieve_bills(state):
    # Retrieve bills for specified state
    bills = retrieve_state_bills(state)

    # Display bills
    print(f'Bills for {state}:')
    for bill in bills:
        print(f'- {bill}')


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
state = "wa"
url = f"https://api.legiscan.com/?key=ddac7961c52b60e13aeba110f6532bc3&op=getMasterList&state=wa"
response: object = urllib.request.urlopen(url)
x = urllib.request.urlopen(url)
data = json.loads(response.read().decode())
print(data)
print(x.read())

if __name__ == '__main__':
    # Parse command-line arguments
    if len(sys.argv) != 2:
        print('Usage: python retrieve_bills2.py <state>')
        sys.exit(1)
    state = sys.argv[1]

    # Call main function
    retrieve_bills(state)
# %%
