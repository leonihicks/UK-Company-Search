#GUI for company_search program
 
#To-do:
#Complete table ^
#Check at least one result is returned
#Have fresh results - i.e. when you type in something new you cannot see the previous company behind


#         Company Name
#         Company Number
#         Date of incorporation
#         Jurisdiction (EW/SC/NI)
#         Trading Status (e.g. Active)
#         Action Code (Companies in certain action codes)
#         Company types (Limited /plc / cic / llp etc)
#         Accounts overdue
#         CS01 overdue
 
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

           ## TODO - as cli get default values
           'title': company_data_api['items'][i]['title'],
           'company_number': company_data_api['items'][i]['company_number'],
     #      'date_of_incorportation': company_data_api['items'][i]['date_of_incorportation'],
      #     'company_jurisdiction': company_data_api['items'][i]['company_jurisdiction'],
           'company_status': company_data_api['items'][i].get('company_status','missing'),
          # 'action_code': company_data_api['items'][i]['action_code'],
         #  'company_type': company_data_api['items'][i]['company_type'],
        #   'accounts_overdue': company_data_api['items'][i]['accounts_overdue'],
    #       'CS01_overdue': company_data_api['items'][i]['CS01_overdue']
        }


        companies.append(company)
        i = i + 1
   
    return companies

# Creating a function for a button
def button_click():
    entered_text = entry1.get()
    status_text.delete(0.0, END)
    try:
        company_results = search_api(entered_text)
    except:
        company_results = 'ERROR',"Company not found."
    status_text.insert(END, company_results[0] + " - " + str(company_results[1]) + " records available")

    # Display total results
    num_data_records = len(company_results[2])
 
    for i in range(num_data_records):
        for j in range(3):
            frame = Frame(
                master=window,
                relief=RAISED,
                borderwidth=1
            )
            frame.grid(row=7 + i, column=j, sticky=W)
            if j == 0:
                data = company_results[2][i].get('title')
            elif j == 1:
                data = company_results[2][i].get('company_number')
            else:
                data = company_results[2][i].get('company_status')
            label = Label(master=frame, text=data)
            label.pack()


 
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
 
 
## --- Infinate loop
window.mainloop()
