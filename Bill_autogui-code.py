import tkinter as tk
import sqlite3
import csv
from tkinter import filedialog, messagebox, simpledialog

url = "https://apps.leg.wa.gov/billinfo/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract bill titles and summaries
bill_titles = []
bill_summaries = []

for bill in soup.find_all('div', class_='bill'):
    title = bill.find('h2').text.strip()
    summary = bill.find('p').text.strip()
    bill_titles.append(title)
    bill_summaries.append(summary)

# Save bill information to a CSV file
import csv

with open('bills.csv', mode='w') as bill_file:
    bill_writer = csv.writer(bill_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(bill_titles)):
        bill_writer.writerow([bill_titles[i], bill_summaries[i]])

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Define categories and keywords
categories = {
    "Education": ["school", "teacher", "student", "college"],
    "Healthcare": ["health", "doctor", "insurance", "hospital"],
    "Taxes": ["tax", "revenue", "budget", "funding"],
    "Work": ["right to repair", "living wage", "Paid Family Leave"]
}

# Tokenize bill summaries and categorize based on keywords
bill_categories = []
stop_words = set(stopwords.words('english'))

for summary in bill_summaries:
    tokens = word_tokenize(summary.lower())
    category_match = False

    for category, keywords in categories.items():
        keyword_match = any(keyword in tokens and keyword not in stop_words for keyword in keywords)
        if keyword_match:
            bill_categories.append(category)
            category_match = True
            break

    if not category_match:
        bill_categories.append("Other")
import tkinter as tk

# Create UI window
root = tk.Tk()
root.title("Bills Tracker")

# Create listbox to display bills
bill_listbox = tk.Listbox(root)
for i in range(len(bill_titles)):
    bill_listbox.insert(tk.END, f"{bill_titles[i]} ({bill_categories[i]})")
bill_listbox.pack()

# Create search bar to filter bills by keyword
search_var = tk.StringVar()
search_var.trace("w", lambda name, index, mode, sv=search_var: filter_bills())
search_entry = tk.Entry(root, textvariable=search_var)
search_entry.pack()

# Create function to filter bills by keyword
def filter_bills():
    keyword = search_var.get().lower()
    bill_listbox.delete(0, tk.END)
    for i in range(len(bill_titles)):
        if keyword in bill_titles[i].lower() or keyword in bill_summaries[i].lower():
            bill_listbox.insert(tk.END, f"{bill_titles[i]} ({bill_categories[i]})")

root.mainloop()
import requests

# Define API endpoints
bill_api_url = "https://www.example-state-legislature.com/api/bills"
news_api_url = "https://www.example-news-outlet.com/api/news"

# Fetch bill updates
bill_updates = []
for bill in bill_titles:
    response = requests.get(f"{bill_api_url}/{bill}")
    if response.status_code == 200:
        status = response.json()['status']
        bill_updates.append(f"{bill}: {status}")
    else:
        bill_updates.append(f"{bill}: Error fetching bill status")

# Fetch news related to bills
news_articles = []
for category in categories:
    response = requests.get(f"{news_api_url}?category={category}")
    if response.status_code == 200:
        articles = response.json()['articles']
        for article in articles:
            news_articles.append(article['title'])
    else:
        news_articles.append(f"Error fetching news for {category}")
import smtplib

# Define email settings
smtp_server = "smtp.example.com"
smtp_port = 587
smtp_username = "you@example.com"
smtp_password = "yourpassword"

# Define email message
message = "Subject: Bill Update\n\nA bill you are tracking has been updated."

# Define function to send email alerts
def send_email_alert(email, message):
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email, message)

# Check for bill updates and send email alerts
tracked_bills = ["Education Bill", "Healthcare Bill"]
for bill in tracked_bills:
    response = requests.get(f"{bill_api_url}/{bill}")
    if response.status_code == 200:
        status = response.json()['status']
        if status != "Introduced":
            send_email_alert("youremail@example.com", message)
    else:
        print(f"Error fetching status for {bill}")
import sqlite3

# Define database connection and cursor
conn = sqlite3.connect('bills.db')
c = conn.cursor()

# Create bills table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS bills
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT,
              description TEXT,
              category TEXT,
              state TEXT)''')

# Insert bills into database
for bill in bills:
    c.execute(f"INSERT INTO bills (title, description, category, state) VALUES (?, ?, ?, ?)",
              (bill['title'], bill['description'], bill['category'], bill['state']))

# Commit changes and close connection
conn.commit()
conn.close()
import tkinter as tk

# Define function to display bill details
def display_bill_details(title, description):
    details_window = tk.Toplevel(root)
    details_window.title(title)
    details_window.geometry("400x400")

    title_label = tk.Label(details_window, text=title, font=("Arial", 16))
    title_label.pack(pady=10)

    description_label = tk.Label(details_window, text=description, font=("Arial", 12))
    description_label.pack(pady=10)

# Create GUI
root = tk.Tk()
root.title("Bill Tracker")

# Define bill listbox
bill_listbox = tk.Listbox(root, width=50, height=20)
bill_listbox.pack(padx=10, pady=10)

# Populate bill listbox with bills
for bill in bills:
    bill_listbox.insert(tk.END, bill['title'])

# Define bill details button
details_button = tk.Button(root, text="View Details", command=lambda: display_bill_details(bill_listbox.get(tk.ACTIVE), bill_listbox.get(tk.ACTIVE)))
details_button.pack(pady=10)

# Start GUI
root.mainloop()
# Define function to search bills
def search_bills(query):
    search_results = []
    for bill in bills:
        if query.lower() in bill['title'].lower() or query.lower() in bill['description'].lower():
            search_results.append(bill['title'])
    return search_results

# Define search function for GUI
def search_bills_gui():
    query = search_entry.get()
    results = search_bills(query)
    bill_listbox.delete(0, tk.END)
    for result in results:
        bill_listbox.insert(tk.END, result)

# Add search bar to GUI
search_frame = tk.Frame(root)
search_frame.pack(padx=10, pady=10)

search_label = tk.Label(search_frame, text="Search Bills:", font=("Arial", 12))
search_label.pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT)

search_button = tk.Button(search_frame, text="Search", command=search_bills_gui)
search_button.pack(side=tk.LEFT)

# Define function to add bill to database
def add_bill(title, description, category, state):
    # Open database connection and cursor
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()

    # Insert new bill into database
    c.execute(f"INSERT INTO bills (title, description, category, state) VALUES (?, ?, ?, ?)",
              (title, description, category, state))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Define function for adding new bill in GUI
def add_bill_gui():
    # Define new bill window
    new_bill_window = tk.Toplevel(root)
    new_bill_window.title("Add New Bill")
    new_bill_window.geometry("400x400")

    # Define new bill form
    title_label = tk.Label(new_bill_window, text="Title:")
    title_label.pack(pady=10)

    title_entry = tk.Entry(new_bill_window, width=30)
    title_entry.pack(pady=10)

    description_label = tk.Label(new_bill_window, text="Description:")
    description_label.pack(pady=10)

    description_entry = tk.Entry(new_bill_window, width=30)
    description_entry.pack(pady=10)

    category_label = tk.Label(new_bill_window, text="Category:")
    category_label.pack(pady=10)

    category_entry = tk.Entry(new_bill_window, width=30)
    category_entry.pack(pady=10)

    state_label = tk.Label(new_bill_window, text="State:")
    state_label.pack(pady=10)

    state_entry = tk.Entry(new_bill_window, width=30)
    state_entry.pack(pady=10)

    # Define function for adding new bill to database
    def add_new_bill():
        add_bill(title_entry.get(), description_entry.get(), category_entry.get(), state_entry.get())
        new_bill_window.destroy()

    # Define button for adding new bill to database
    add_button = tk.Button(new_bill_window, text="Add Bill", command=add_new_bill)
    add_button.pack(pady=10)
# Define function to update bill in database
def update_bill(title, description, category, state, bill_id):
    # Open database connection and cursor
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()

    # Update bill in database
    c.execute(f"UPDATE bills SET title=?, description=?, category=?, state=? WHERE id=?",
              (title, description, category, state, bill_id))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Define function for editing existing bill in GUI
def edit_bill_gui():
    # Get selected bill from listbox
    selected_bill = bill_listbox.get(tk.ACTIVE)

    # Get bill details from database
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM bills WHERE title=?", (selected_bill,))
    bill = c.fetchone()
    conn.close()

    # Define edit bill window
    edit_bill_window = tk.Toplevel(root)
    edit_bill_window.title("Edit Bill")
    edit_bill_window.geometry("400x400")

    # Define edit bill form
    title_label = tk.Label(edit_bill_window, text="Title:")
    title_label.pack(pady=10)

    title_entry = tk.Entry(edit_bill_window, width=30)
    title_entry.insert(0, bill[1])
    title_entry.pack(pady=10)

    description_label = tk.Label(edit_bill_window, text="Description:")
    description_label.pack(pady=10)

    description_entry = tk.Entry(edit_bill_window, width=30)
    description_entry.insert(0, bill[2])
    description_entry.pack(pady=10)

    category_label = tk.Label(edit_bill_window, text="Category:")
    category_label.pack(pady=10)

    category_entry = tk.Entry(edit_bill_window, width=30)
    category_entry.insert(0, bill[3])
    category_entry.pack(pady=10)

    state_label = tk.Label(edit_bill_window, text="State:")
    state_label.pack(pady=10)

    state_entry = tk.Entry(edit_bill_window, width=30)
    state_entry.insert(0, bill[4])
    state_entry.pack(pady=10)

    # Define function for updating existing bill in database
    def update_existing_bill():
        update_bill(title_entry.get(), description_entry.get(), category_entry.get(), state_entry.get(), bill[0])
        edit_bill_window.destroy()

    # Define button for updating existing bill in database
    update_button = tk.Button(edit_bill_window, text="Update Bill", command=update_existing_bill)
    update_button.pack(pady=10)

# Define function to delete bill from database
def delete_bill(bill_id):
    # Open database connection and cursor
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()

    # Delete bill from database
    c.execute(f"DELETE FROM bills WHERE id=?", (bill_id,))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Define function for deleting bill in GUI
def delete_bill_gui():
    # Get selected bill from listbox
    selected_bill = bill_listbox.get(tk.ACTIVE)

    # Get bill details from database
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM bills WHERE title=?", (selected_bill,))
    bill = c.fetchone()
    conn.close()

    # Ask user to confirm deletion
    confirm_delete = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {selected_bill}?")

    # Delete bill if user confirms deletion
    if confirm_delete:
        delete_bill(bill[0])
        bill_listbox.delete(tk.ACTIVE)
# Define function to search bills in database
def search_bills(search_query):
    # Open database connection and cursor
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()

    # Search bills in database
    c.execute(f"SELECT * FROM bills WHERE title LIKE ? OR description LIKE ? OR category LIKE ? OR state LIKE ?",
              (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
    bills = c.fetchall()

    # Close connection and return search results
    conn.close()
    return bills

# Define function for searching bills in GUI
def search_bills_gui():
    # Define search bills window
    search_bills_window = tk.Toplevel(root)
    search_bills_window.title("Search Bills")
    search_bills_window.geometry("400x400")

    # Define search bills form
    search_label = tk.Label(search_bills_window, text="Search:")
    search_label.pack(pady=10)

    search_entry = tk.Entry(search_bills_window, width=30)
    search_entry.pack(pady=10)

    # Define function for displaying search results in listbox
    def display_search_results():
        search_results = search_bills(search_entry.get())
        bill_listbox.delete(0, tk.END)
        for bill in search_results:
            bill_listbox.insert(tk.END, bill[1])

    # Define button for searching bills
    search_button = tk.Button(search_bills_window, text="Search", command=display_search_results)
    search_button.pack(pady=10)
# Define function to sort bills in database
def sort_bills(sort_query):
    # Open database connection and cursor
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()

    # Sort bills in database
    c.execute(f"SELECT * FROM bills ORDER BY {sort_query}")
    bills = c.fetchall()

    # Close connection and return sorted results
    conn.close()
    return bills

# Define function for sorting bills in GUI
def sort_bills_gui():
    # Define sort bills window
    sort_bills_window = tk.Toplevel(root)
    sort_bills_window.title("Sort Bills")
    sort_bills_window.geometry("400x400")

    # Define sort bills form
    sort_label = tk.Label(sort_bills_window, text="Sort by:")
    sort_label.pack(pady=10)

    sort_options = ["title", "description", "category", "state"]
    sort_variable = tk.StringVar(sort_bills_window)
    sort_variable.set(sort_options[0])

    sort_dropdown = tk.OptionMenu(sort_bills_window, sort_variable, *sort_options)
    sort_dropdown.pack(pady=10)

    # Define function for displaying sorted results in listbox
    def display_sorted_results():
        sorted_results = sort_bills(sort_variable.get())
        bill_listbox.delete(0, tk.END)
        for bill in sorted_results:
            bill_listbox.insert(tk.END, bill[1])

    # Define button for sorting bills
    sort_button = tk.Button(sort_bills_window, text="Sort", command=display_sorted_results)
    sort_button.pack(pady=10)

# Define function to export bills to CSV file
def export_bills():
    # Open database connection and cursor
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()

    # Export bills to CSV file
    c.execute("SELECT * FROM bills")
    bills = c.fetchall()
    with open('bills.csv', mode='w', newline='') as bills_file:
        writer = csv.writer(bills_file)
        writer.writerow(['Title', 'Description', 'Category', 'State', 'Introduced', 'Status', 'Link'])
        for bill in bills:
            writer.writerow([bill[1], bill[2], bill[3], bill[4], bill[5], bill[6], bill[7]])

    # Close connection and notify user of successful export
    conn.close()
    messagebox.showinfo("Export Success", "Bills exported to bills.csv file.")

# Define function for exporting bills in GUI
def export_bills_gui():
    # Call function to export bills to CSV file
    export_bills()

    # Define function to import bills from CSV file
def import_bills():
    # Open database connection and cursor
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()

    # Prompt user to select CSV file
    filename = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    if filename:
        # Clear existing bills in database
        c.execute("DELETE FROM bills")

        # Import bills from CSV file
        with open(filename, mode='r') as bills_file:
            reader = csv.DictReader(bills_file)
            for row in reader:
                bill_data = (row['Title'], row['Description'], row['Category'], row['State'], row['Introduced'], row['Status'], row['Link'])
                c.execute("INSERT INTO bills VALUES (NULL,?,?,?,?,?,?,?)", bill_data)

        # Close connection and notify user of successful import
        conn.commit()
        conn.close()
        messagebox.showinfo("Import Success", "Bills imported from CSV file.")

# Define function for importing bills in GUI
def import_bills_gui():
    # Call function to import bills from CSV file
    import_bills()

# Define function to search bills by title or description
def search_bills(keyword):
    # Open database connection and cursor
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()

    # Search bills by title or description
    c.execute("SELECT * FROM bills WHERE Title LIKE ? OR Description LIKE ?", ('%'+keyword+'%', '%'+keyword+'%'))
    bills = c.fetchall()

    # Close connection and return search results
    conn.close()
    return bills

# Define function for searching bills in GUI
def search_bills_gui():
    # Prompt user for keyword to search by
    keyword = simpledialog.askstring("Search", "Enter keyword to search bills by:")

    # Search bills by keyword and display results in a new window
    if keyword:
        bills = search_bills(keyword)
        if bills:
            search_window = Toplevel(root)
            search_window.title("Search Results")
            scrollbar = Scrollbar(search_window)
            scrollbar.pack(side=RIGHT, fill=Y)
            listbox = Listbox(search_window, yscrollcommand=scrollbar.set)
            for bill in bills:
                listbox.insert(END, bill[1])
            listbox.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.config(command=listbox.yview)
        else:
            messagebox.showinfo("No Results", "No bills found with the keyword '"+keyword+"'.")

