import tkinter as tk

def check_login():
    print("Login button clicked")

# Create the main application window
login_window = tk.Tk()
login_window.title("Login Window")

# Create a username label and entry
tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
username_entry = tk.Entry(login_window)
username_entry.grid(row=0, column=1, padx=10, pady=(10, 0))

# Create a password label and entry
tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
password_entry = tk.Entry(login_window, show='*')
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Create a login button
tk.Button(login_window, text="Login", command=check_login).grid(row=2, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
login_window.mainloop()
