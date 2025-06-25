import tkinter as tk 
from tkinter import messagebox

#check config
vpn_on = False
def connect_to_vpn():
    global vpn_on
    #store data for username,password and ip 
    server_address = entry_server.get()
    username = entry_username.get()
    password = entry_password.get()

    if server_address and username and password and vpn_on == False:
     #connection to vpn server
     messagebox.showinfo("Connected","Connect to VPN Server")
     vpn_on = True
    else:
     messagebox.showerror("Error","Please input the right information")

def disconnect_from_vpn():
  global vpn_on
  server_address = entry_server.get()
  username = entry_username.get()
  password = entry_password.get()
  if server_address and username and password and vpn_on == 1:
    messagebox.showerror("Disconnected","You have been Disconnected")
    vpn_on = False
  else:
    messagebox.showerror("Error","You are not connected")


#Main Window  
window = tk.Tk()
window.title(" VPN ")

#window config
wrdtbox = 5
windowwidth = 30


#server add/ip
label_server = tk.Label(window, text= "Server Address(IP)")
label_server.pack(pady=wrdtbox)
entry_server = tk.Entry(window,width=windowwidth)
entry_server.pack(pady=wrdtbox)

#user
label_username = tk.Label(window, text= "Username")
label_username.pack(pady=wrdtbox)
entry_username = tk.Entry(window,width=windowwidth)
entry_username.pack(pady=wrdtbox)

#pass
label_password = tk.Label(window, text= "Password")
label_password.pack(pady=wrdtbox)
entry_password = tk.Entry(window,show="*",width=windowwidth)
entry_password.pack(pady=wrdtbox)

connect_button = tk.Button(window, text="Connect", command = connect_to_vpn)
connect_button.pack(pady=10)

disconnect_button = tk.Button(window, text="Disconnect", command = disconnect_from_vpn)
disconnect_button.pack(pady=10)
window.mainloop()
