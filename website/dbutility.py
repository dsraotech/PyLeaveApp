import tkinter as tk
from tkinter import messagebox
from getpass import getpass

# Sample user credentials
users = {
    'admin': 'password123',
    'user1': 'pass123'
}

# Function to check login credentials
def check_login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username in users and users[username] == password:
        login_window.destroy()
        show_main_menu()
    else:
        messagebox.showerror("Login Error", "Invalid username or password")

# Function to show the main menu
def show_main_menu():
    main_menu = tk.Tk()
    main_menu.title("Main Menu")
    
    tk.Label(main_menu, text="Select an option:").pack(pady=10)
    
    tk.Button(main_menu, text="1. Leave Entry", command=leave_entry).pack(pady=5)
    tk.Button(main_menu, text="2. Leave Modification", command=leave_modification).pack(pady=5)
    tk.Button(main_menu, text="3. Leave Cancel", command=leave_cancel).pack(pady=5)
    tk.Button(main_menu, text="4. Report", command=report).pack(pady=5)
    tk.Button(main_menu, text="5. Exit", command=main_menu.destroy).pack(pady=5)
    
    main_menu.mainloop()

# Function to handle leave entry
def leave_entry():
    entry_window = tk.Toplevel()
    entry_window.title("Leave Entry")
    tk.Label(entry_window, text="Enter leave details here...").pack(pady=10)
    # Add more widgets as needed
    tk.Button(entry_window, text="Submit", command=entry_window.destroy).pack(pady=5)

# Function to handle leave modification
def leave_modification():
    modification_window = tk.Toplevel()
    modification_window.title("Leave Modification")
    tk.Label(modification_window, text="Modify leave details here...").pack(pady=10)
    # Add more widgets as needed
    tk.Button(modification_window, text="Submit", command=modification_window.destroy).pack(pady=5)

# Function to handle leave cancel
def leave_cancel():
    cancel_window = tk.Toplevel()
    cancel_window.title("Leave Cancel")
    tk.Label(cancel_window, text="Cancel leave details here...").pack(pady=10)
    # Add more widgets as needed
    tk.Button(cancel_window, text="Submit", command=cancel_window.destroy).pack(pady=5)

# Function to handle report generation
def report():
    report_window = tk.Toplevel()
    report_window.title("Report")
    tk.Label(report_window, text="Generate report here...").pack(pady=10)
    # Add more widgets as needed
    tk.Button(report_window, text="Generate", command=report_window.destroy).pack(pady=5)

# Create the login window
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Username:").pack(pady=5)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

tk.Label(login_window, text="Password:").pack(pady=5)
password_entry = tk.Entry(login_window, show='*')
password_entry.pack(pady=5)

tk.Button(login_window, text="Login", command=check_login).pack(pady=10)

login_window.mainloop()
