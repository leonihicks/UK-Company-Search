#GUI for company_search program

from tkinter import *
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
        return 'ERROR','Please set the environment variable CH_API_KEY which should contain your API Key for Companies House API'
       
    payload = {'q': search_string}
 
    # Call API
    server_address = 'https://api.companieshouse.gov.uk'
    url = server_address + '/search/companies'
    r = requests.get(url, params=payload, auth=(api_key, ''))
    if r.status_code != requests.codes.ok:
        return 'ERROR','Error HTTP Status [' + str(r.status_code) + '] from ' + url
 
    companyData = r.json()
    return 'OK', companyData
 
# Creating a function for a button
def button_click():
    entered_text = entry1.get()
    output_text.delete(0.0, END)
    status_text.delete(0.0, END)
    try:
        company = search_api(entered_text)
    except:
        company = 'ERROR',"Company not found."
    status_text.insert(END, company[0])
    output_text.insert(END, company[1])
 
### ---------------- Main Code
 
## Steps
# - Have Status and Data table
 
## --- Setup GUI
 
#Query User to input their answer
Label(window, text="Enter company you want to search with: ").grid(row=0, column=0, sticky=W)
 
# Entry box for users input
entry1=Entry(window, width=20, bg="light blue")
entry1.grid(row=1, column=0,sticky=W)
 
#
# Creating a button for user to submit answer written
Button(window, text="SUBMIT", width=5, command=button_click).grid(row=2, column=0, sticky=W)
 
# Creating an text box for API status to be  displayed
status_text = Text(window, width=50, height=2, wrap=WORD, background= "light blue")
status_text.grid(row=3, column=0, columnspan=2, sticky=W)
 
# Creating an output text box for data to be displayed
output_text = Text(window, width=50, height=20, wrap=WORD, background= "light blue")
output_text.grid(row=5, column=0, columnspan=2, sticky=W)
 
# Print out key data from first company returned from the search - companyData['items'][0] into output text
companyResults = {"('TOP RESULT for search' + (search_string))",
                  "('Title: ' + companyData['items'][0]['title'])",
                  "('Company Number: ' + companyData['items'][0]['company_number'])",
                  "('Status: ' + companyData['items'][0]['company_status'])",
                  "('Date of Creation: ' + companyData['items'][0]['date_of_creation'])",
                  "('Address: ')",
                  "(companyData['items'][0]['address'].get('premises', 'No premise found'))",
                  "(companyData['items'][0]['address'].get('address_line_1', 'No address line 1found'))",
                  "(companyData['items'][0]['address'].get('locality', 'No locality found'))",
                  "(companyData['items'][0]['address'].get('region', 'No region found'))",
                  "(companyData['items'][0]['address'].get('postal_code', 'No post code found'))"}
 
## --- Infinate loop
 
window.mainloop()
