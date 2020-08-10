# UK-Company-Search

## Description 

A GUI python program to search UK companies with an optional filter for company status. 

In the search text you can either enter
- The company name (a list of results will be returned)
- The company number (just that company will be returned)


## Set up for Windows

Download python 3.7 from the Microsoft store (Windows 10)

Open Command Prompt

pip3 install requests python3 company_search_GUI.py

 

``` bash

pip3 install requests

python3 company_search_GUI.py

```


## Environmental variables

The following is a list of environment variables for the service to run:
 
Name                    | Description               | Mandatory ?
---------------------- | -------------------------  | ------------------------
CH_API_KEY        | CHS API key              | YES
CHS_BASE_URL  | CHS Server URL        | NO  (default = api.companieshouse.gov.uk)