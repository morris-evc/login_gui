import pandas as pd
import tkinter
from tkinter import *
from tkinter.constants import END 
from tkinter import Text, messagebox
from tkinter import ttk
import mysql.connector
pd.options.display.max_colwidth = 200
#pd.set_option('display.max_columns', None)


#Database connection
mydb = mysql.connector.connect(
    host="logins.c7dzlgckel62.us-east-1.rds.amazonaws.com",
    user="admin",
    password="MUCH-llc2020!",
    database="Logins"
)
mycursor = mydb.cursor()

#DB call for client list
client_query = "SELECT DISTINCT Client_Name FROM Master_Accounts ORDER BY Client_Name ASC"
mycursor.execute(client_query)
client_result = mycursor.fetchall()
c_list = []
for c in client_result:
    c_list.append(c[0])


#DB call for vendor list
vendor_query = "SELECT DISTINCT Vendor FROM Master_Accounts ORDER BY Vendor ASC "
mycursor.execute(vendor_query)
vendor_result = mycursor.fetchall()
v_list = []

for v in vendor_result:
    v_list.append(v[0])


#Empty lists to store accounts
multi_accts_list = []
single_accts_list = []

#Define window
root = tkinter.Tk()
root.title('Access Database')
root.geometry('1500x500')
root.resizable(0,0)

#Functions

#Search for account
def search_for():
    if len(account_entry.get()) != 0:
        acct_num_query  ="SELECT Account_Number, Username, Password, Utility_Company, Vendor_URL FROM Master_Accounts WHERE Account_Number LIKE '%{}'".format(account_entry.get())
        mycursor.execute(acct_num_query)
        acct_num_result = mycursor.fetchall()
        for num in acct_num_result:
            single_accts_list.append(num)

        acct_df =  pd.DataFrame(single_accts_list)
        acct_df.columns = [[ 'Account No.', 'Username', 'Password', 'Vendor', 'Vendor URL']]
        #acct_df.style.hide_index()
        results_txt.insert('1.0', acct_df)
        results_txt.pack()
    elif client_input.get() == "Client" or vend_input.get() == "Vendor":
        messagebox.askretrycancel("WARNING", "Please select a client and vendor.")
    else:
        print("test")
        account_query = "SELECT Account_Number, Username, Password, Utility_Company, Vendor_URL FROM Master_Accounts WHERE Client_Name = '{}' AND Vendor = '{}' ".format(client_input.get(), vend_input.get())
        mycursor.execute(account_query)
        account_result = mycursor.fetchall()
        print(account_query)
        for x in account_result:
            multi_accts_list.append(x)
        df = pd.DataFrame(multi_accts_list)
        df.columns = ['Account No.', 'Username', 'Password', 'Vendor', 'Vendor URL']
        #df.style.hide_index()
        results_txt.insert('1.0', df)

    

#Clear input fields
def clear_input():
    account_entry.delete(0, END)
    client_input.set('Client')
    vend_input.delete(0, END)
    results_txt.delete('1.0', END)
    client_input.set("Client")
    vend_input.set("Vendor")
    single_accts_list.clear()
    multi_accts_list.clear()

#Define frames
input_frame = tkinter.Frame(root, bg='#03191E', width=1490, height=150)
output_frame = tkinter.Frame(root, bg='#E8C547', width=500, height=400)
results_txt = tkinter.Text(output_frame, width=490, height=490)
input_frame.pack(padx=10, pady=10)
output_frame.pack(padx=10, pady=(0,10))
results_txt.pack(padx=10, pady=10)

#Account no. input
account_entry = tkinter.Entry(input_frame, width=40)
account_entry.grid(row=0, column=0, padx=5, pady=5)
#account_entry.insert(0, "Account Number")
account_label = tkinter.Label(input_frame, width=15, bg='#03191E', fg='#FFFFFF', text= 'Account No.')
account_label.grid(row=0, column=1, padx=5, pady=5)



#Client input
client_input = ttk.Combobox(input_frame, width=35, values=c_list)
client_input.grid(row=1, column=0, padx=5, pady=5)
client_input.set('Client')

#Vendor input
vend_input = ttk.Combobox(input_frame, width=35, values=v_list)
vend_input.grid(row=2, column=0, padx=5, pady=5)
vend_input.set('Vendor')



#this line (_propagate) will keep the frame from resizing to the widget
input_frame.grid_propagate(0)

#Define buttons
search_btn = tkinter.Button(input_frame, text='Search', command=search_for)
search_btn.grid(row=4,column=0, padx=1, pady=1, ipadx=25)

clear_btn = tkinter.Button(input_frame, text='Clear', command=clear_input)
clear_btn.grid(row=5,column=0, padx=1, pady=1, ipadx=29)


#Run root window's mainloop
root.mainloop()