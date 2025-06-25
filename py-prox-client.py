import tkinter as tk 
from tkinter import messagebox
import requests

# Check config
proxy_on = False
proxies = {}

def connect_to_proxy():
    global proxy_on, proxies
    server_address = entry_server.get()
    port = entry_port.get()
    username = entry_username.get()
    password = entry_password.get()

    if server_address and port and username and password and not proxy_on:
        proxies = {
            "http": f"http://{username}:{password}@{server_address}:{port}",
            "https": f"https://{username}:{password}@{server_address}:{port}"
        }
        # Test connection
        try:
            response = requests.get("http://httpbin.org/ip", proxies=proxies)
            if response.status_code == 200:
                messagebox.showinfo("Connected", "Connected to Proxy Server")
                proxy_on = True
            else:
                messagebox.showerror("Error", "Failed to connect to Proxy Server")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please input the right information")

def disconnect_from_proxy():
    global proxy_on
    if proxy_on:
        messagebox.showinfo("Disconnected", "You have been Disconnected from Proxy")
        proxy_on = False
    else:
        messagebox.showerror("Error", "You are not connected")

# Main Window  
window = tk.Tk()
window.title("Proxy Connection")

# Window config
wrdtbox = 5
windowwidth = 30

# Server address
label_server = tk.Label(window, text="Server Address")
label_server.pack(pady=wrdtbox)
entry_server = tk.Entry(window, width=windowwidth)
entry_server.pack(pady=wrdtbox)

# Port
label_port = tk.Label(window, text="Port")
label_port.pack(pady=wrdtbox)
entry_port = tk.Entry(window, width=windowwidth)
entry_port.pack(pady=wrdtbox)

# User
label_username = tk.Label(window, text="Username")
label_username.pack(pady=wrdtbox)
entry_username = tk.Entry(window, width=windowwidth)
entry_username.pack(pady=wrdtbox)

# Password
label_password = tk.Label(window, text="Password")
label_password.pack(pady=wrdtbox)
entry_password = tk.Entry(window, show="*", width=windowwidth)
entry_password.pack(pady=wrdtbox)

connect_button = tk.Button(window, text="Connect", command=connect_to_proxy)
connect_button.pack(pady=10)

disconnect_button = tk.Button(window, text="Disconnect", command=disconnect_from_proxy)
disconnect_button.pack(pady=10)

window.mainloop()