import tkinter as tk

def check_login():
    print("Login button clicked")

# Create the main application window
login_window = tk.Tk()
login_window.title("Login Window")

# Create a username label and entry
tk.Label(login_window, text="Username:").place(x=20, y=20)
username_entry = tk.Entry(login_window)
username_entry.place(x=100, y=20, width=150)

# Create a password label and entry
tk.Label(login_window, text="Password:").place(x=20, y=60)
password_entry = tk.Entry(login_window, show='*')
password_entry.place(x=100, y=60, width=150)

# Create a login button
tk.Button(login_window, text="Login", command=check_login).place(x=100, y=100)

# Start the Tkinter event loop
login_window.mainloop()
