#GUI for company_search program
 
#to-do:

#finish code
#add padding -make it look better
#scroll bar

from tkinter import *
import tkinter as tk

window = Tk()
window.title("Companies House GUI search")

import json
import os
import requests
import sys
     
 
### --------------- Functions
def search_api(search_string):
    api_key = os.environ.get('CH_API_KEY')
    if api_key == None:
        return 'ERROR', 0,'Please set the environment variable CH_API_KEY which should contain your API Key for Companies House API'
     
    payload = {'q': search_string, 'items_per_page':30}
 
# Call API
    chs_base_url = os.environ.get('CHS_BASE_URL')
    if chs_base_url == None:
        chs_base_url = "api.companieshouse.gov.uk"
    server_address = 'https://'  + chs_base_url
    url = server_address + '/search/companies'
    r = requests.get(url, params=payload, auth=(api_key, ''))
    if r.status_code != requests.codes.ok:
        return 'ERROR', 0, 'Error HTTP Status [' + str(r.status_code) + '] from ' + url
    company_data_api = r.json()
    return 'OK', company_data_api['total_results'], transform_company_data_api_to_display(company_data_api)

def transform_company_data_api_to_display(company_data_api):
    companies = []
    if company_data_api['total_results'] == 0:
        return companies
    sum_records = 30
    if company_data_api['total_results'] < 30:
        sum_records = company_data_api['total_results']
    i = 0
    while i < sum_records:

        company_number = company_data_api['items'][i].get('company_number','missing')
        status, company_profile_api = get_company_profile(company_number)
        
        company = {
 
            'title': company_data_api['items'][i]['title'],
            'company_number': company_number,
            'date_of_creation': company_data_api['items'][i].get('date_of_creation','missing'),
            'address_snippet': company_data_api['items'][i].get('address_snippet','missing'),
            'jurisdiction': company_profile_api['jurisdiction'],
            'company_status': company_data_api['items'][i].get('company_status','missing'),
            'type': company_profile_api['type'],
            'accounts_overdue': accounts_overdue(company_profile_api),
            'CS_overdue': confirmation_statements_overdue(company_profile_api)
        }
 
 
        companies.append(company)
        i = i + 1
  
    return companies

def accounts_overdue(company_profile_api):
    accounts_dict = company_profile_api.get('accounts')
    if accounts_dict == None:
        return 'missing'

    overdue = accounts_dict.get('overdue', 'missing')
    if overdue == 0:
        return 'False'
    elif overdue == 1:
        return 'True'
    else:
        return 'missing'


def confirmation_statements_overdue(company_profile_api):
    cs_dict = company_profile_api.get('confirmation_statement')
    if cs_dict == None:
        return 'missing'

    overdue = cs_dict.get('overdue', 'missing')
    if overdue == 0:
        return 'False'
    elif overdue == 1:
        return 'True'
    else:
        return 'missing'
    
def get_company_profile(company_number):

    api_key = os.environ.get('CH_API_KEY')
    if api_key == None:
        return 'ERROR', 0,'Please set the environment variable CH_API_KEY which should contain your API Key for Companies House API'
    
    chs_base_url = os.environ.get('CHS_BASE_URL')
    if chs_base_url == None:
        chs_base_url = "api.companieshouse.gov.uk"
    server_address = 'https://'  + chs_base_url
    url = server_address + '/company/' + company_number
    r = requests.get(url, auth=(api_key, ''))
    
    if r.status_code != requests.codes.ok:
        return 'ERROR', 'Error HTTP Status [' + str(r.status_code) + '] from ' + url
    company_profile_api= r.json()
    return 'OK', company_profile_api

    
    
def remove_old_frames():
      
    for f in old_frames:
        for widget in f.winfo_children():
            widget.destroy()
    old_frames.clear()   
 
def populate_heading():
    for j in range(8):
        frame = Frame(
            master=window,
            borderwidth=1
        )
        old_frames.append(frame)
        frame.grid(row=7, column=j, sticky=W, padx =(10,10))
        if j == 0:
            data = "Company Name"
        elif j == 1:
            data = "Number"
        elif j == 2:
            data = "Status" 
        elif j == 3:
            data = "Address"
        elif j ==4:
            data = "Jurisdiction"
        elif j ==5:
            data = "Accounts Overdue"
        elif j == 6:
            data = "CS Overdue"
        else:
            data = "Date of Creation"
        label = Label(master=frame, text=data)
        label.pack()


def trim_string(data,size):
    if data == None:
        return 'missing'
    else:
        return data[:size]
    
def populate_companies(companies):
 
    num_data_records = len(companies)
    for i in range(num_data_records):
        for j in range(8):
            frame = Frame(
                master=window,
                borderwidth=1
            )
            old_frames.append(frame)
            frame.grid(row=8 + i, column=j, sticky=W)
            if j == 0:
                data = companies[i].get('title')
                data = trim_string(data, 30)
            elif j == 1:
                data = companies[i].get('company_number')
            elif j == 2:
                data = companies[i].get('company_status')
            elif j == 3:
                data = companies[i].get('address_snippet')
                data = trim_string(data, 50)
            elif j == 4:
                data = companies[i].get('jurisdiction')
            elif j == 5:
                data = companies[i].get('accounts_overdue')
            elif j == 6:
                data = companies[i].get('CS_overdue')
            else:
                data = companies[i].get('date_of_creation')
            label = Label(master=frame, text=data)
            label.pack()


# Creating a function for a button
def button_click():
 
    remove_old_frames()
 
    entered_text = entry1.get()
    status_text.delete(0.0, END)

    try:
        company_results = search_api(entered_text)
    except Exception as e:
        print('Exception ' + str(e))
        company_results = 'ERROR calling API.', 0, []
 
    status_text.insert(END, company_results[0] + " - " + str(company_results[1]) + " records available")
 
    if company_results[1] == 0:
        return
 
    # At least one row of data to display
    populate_heading()
 
    populate_companies(company_results[2])



class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.grid(row=0, column=9, sticky=W)
        self.create_widgets()

    # Create main GUI window
    def create_widgets(self):
        self.search_var = StringVar()
        self.search_var.trace("w", self.update_list)
        self.entry = Entry(self, textvariable=self.search_var, width=13)
        self.lbox = Listbox(self, width=45, height=15)

        self.entry.grid(row=0, column=9, padx=10, pady=3)
        self.lbox.grid(row=0, column=9, padx=10, pady=3)

        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_list()

    def update_list(self, *args):
        search_term = self.search_var.get()

        # Just a generic list to populate the listbox
        lbox_list = ['active', 'liquidation', 'dissolved']

        self.lbox.delete(0, END)

        for item in lbox_list:
                if search_term.lower() in item.lower():
                    self.lbox.insert(END, item)



### ---------------- Main Code
           
## Steps
 
# - Have Status and Data table
 
## --- Setup GUI
 
#Query User to input their answer
 
Label(window, text="Enter company you want to search with: ").grid(row=0, column=0, sticky=W)
Label(window, text="    ").grid(row=0, column=4, sticky=W)
Label(window, text="    ").grid(row=0, column=7, sticky=W)

# Entry box for users input
 
entry1=Entry(window, width=20, bg="light blue")
entry1.grid(row=0, column=1,sticky=W)
 
# Creating a button for user to submit answer written
 
Button(window, text="SUBMIT", width=5, command=button_click, relief= tk.RAISED, fg = "blue").grid(row=0, column= 3, sticky=W)
 
# Creating an text box for API status to be  displayed
 
status_text = Text(window, width=30, height =1.5, wrap=WORD, background= "light blue")
status_text.grid(row=0, column=5, columnspan=2, sticky=W)

#MODES = [
 #       ("Monochrome", "1"),
    #    ("Grayscale", "L"),
   #    ("True color", "RGB"),
  #      ("Color separation", "CMYK"),
 #   ]
#
#v = StringVar()
#v.set("L") # initialize

#for text, mode in MODES:
  #  b = Radiobutton(master, text=text,
  #                  variable=v, value=mode)
  #  b.pack(anchor=W)

# list of any old frames that need to be tidied up after a new query
old_frames = []

## --- Infinate loop
window.mainloop()
