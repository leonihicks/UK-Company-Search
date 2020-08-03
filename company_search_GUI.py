#GUI for company_search program

from tkinter import *
window = Tk()
window.title("Companies House GUI search")

import json
import os
import requests
import sys

#Query User to input their answer 
search_string = Label(window, text="Enter company you want to search with: ").grid(row=0, column=0, sticky=W)
payload = {'q': search_string}

# Read in the Companies House API Key from an environmental variable
api_key = os.environ.get('CH_API_KEY')
if api_key == None:
    print('Please set the environment variable CH_API_KEY which should contain your API Key for Companies House API')
    sys.exit(1)

# Entry box for users input
entry1=Entry(window, width=20, bg="light blue")
entry1.grid(row=1, column=0,sticky=W)

# Creating a function for a button
def button_click():
    entered_text = entry1.get()
    output_text.delete(0.0, END)
    try:
        company = companyResults[entered_text]
    except:
        company = "Company not found."
    output_text.insert(END, company)
  
# Creating a button for user to submit answer written
Button(window, text="SUBMIT", width=5, command=button_click).grid(row=2, column=0, sticky=W)

# Creating an output text box for data to be displayed
output_text = Text(window, width=50, height=6, wrap=WORD, background= "light blue")
output_text.grid(row=3, column=0, columnspan=2, sticky=W)

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

# Call API
server_address = 'https://api.companieshouse.gov.uk'
url = server_address + '/search/companies'
r = requests.get(url, params=payload, auth=(api_key, ''))
if r.status_code != requests.codes.ok:
    print('Error HTTP Status [' + str(r.status_code) + '] from ' + url)
    sys.exit(1)

# Decode JSON into a dictionary
companyData = r.json()




window.mainloop()
