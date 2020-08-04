#GUI for company_search program
 
#To-do:
#Return items in a table (set out as table) - first three
#Complete table ^
#Check at least one result is returned
#Make it beautiful
 
from tkinter import *
import tkinter as tk
from tkinter import ttk
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
        company = {
           'title': company_data_api['items'][i]['title'],
           'company_number': company_data_api['items'][0]['company_number']
        }
        companies.append(company)
        i = i + 1
   
    return companies

#Showing the results
def show(company_data_api):
    temp_list=[companyResults[2]]
    temp_list.sort(key=lambda e: e[1], reverse=True)
    for i, (position, name, h, l) in enumerate(temp_list, start=1):
        results.insert("", "end", values=(i))


# Creating a function for a button
def button_click():
    entered_text = entry1.get()
    status_text.delete(0.0, END)
    try:
        companyResults = search_api(entered_text)
    except:
        companyResults = 'ERROR',"Company not found."
    status_text.insert(END, companyResults[0])
    # Display total results
    results.insert("", "end", values=(companyResults[2]))

### ---------------- Main Code
    
## Steps
    
# - Have Status and Data table

## --- Setup GUI

#Query User to input their answer

Label(window, text="Enter company you want to search with: ").grid(row=0, column=0, sticky=W)

# Entry box for users input

entry1=Entry(window, width=20, bg="light blue")
entry1.grid(row=1, column=0,sticky=W)

# Creating a button for user to submit answer written

Button(window, text="SUBMIT", width=5, command=button_click).grid(row=2, column=0, sticky=W)

# Creating an text box for API status to be  displayed

status_text = Text(window, width=50, height=2, wrap=WORD, background= "light blue")
status_text.grid(row=3, column=0, columnspan=2, sticky=W)

entered_text = entry1.get()
cols = ('Position','Name','h','l')
results = ttk.Treeview(window, columns=cols, show='headings')
companyResults = search_api(entered_text)


for col in cols:
    results.heading(col, text=col, ) 
    results.insert("", "end", values=(companyResults[2]))
results.grid(row=10, column=0, columnspan=4, sticky=W)


 
## --- Infinate loop

window.mainloop()
