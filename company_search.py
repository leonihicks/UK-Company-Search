#!/usr/bin/env python3#!/usr/bin/env python3

"""
Searches the UK Companies house API with an input search string It prints out key data from the first returned item
"""
import json
import os
import requests
import sys

# Read in the Companies House API Key from an environmentalvariable
api_key = os.environ.get('CH_API_KEY')
if api_key == None:
    print('Please set the environment variable CH_API_KEY which should contain your API Key for Companies House API')
    sys.exit(1)

# Read in the query from CLI
search_string = input('Enter company you want to search with: ')
payload = {'q': search_string}

# Call API
server_address = 'https://api.companieshouse.gov.uk'
url = server_address + '/search/companies'
r = requests.get(url, params=payload, auth=(api_key, ''))
if r.status_code != requests.codes.ok:
    print('Error HTTP Status [' + str(r.status_code) + '] from ' + url)
    sys.exit(1)

# Decode JSON into a dictionary
companyData = r.json()

# Print out key data from first company returned from the search - companyData['items'][0]
print('TOP RESULT for search [' + search_string +']')
print('Title: ' + companyData['items'][0]['title'])
print('Company Number: ' + companyData['items'][0]['company_number'])
print('Status: ' + companyData['items'][0]['company_status'])
print('Date of Creation: ' + companyData['items'][0]['date_of_creation'])
print('Address: ')
print(companyData['items'][0]['address'].get('premises', 'No premise found'))
print(companyData['items'][0]['address'].get('address_line_1', 'No address line 1found'))
print(companyData['items'][0]['address'].get('locality', 'No locality found'))
print(companyData['items'][0]['address'].get('region', 'No region found'))
print(companyData['items'][0]['address'].get('postal_code', 'No post code found'))
