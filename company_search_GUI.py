#GUI for company_search program

from tkinter import *
window = Tk()
window.title("Companies House GUI search")

Label(window, text="Enter company you want to search with: ").grid(row=0, column=0, sticky=W)

#if no api key is given display an error message and the print below and to reset the variable and restart the porgram
import json
import os
import requests
import sys

# Read in the Companies House API Key from an environmentalvariable
api_key = os.environ.get('CH_API_KEY')
if api_key == None:
    print('Please set the environment variable CH_API_KEY which should contain your API Key for Companies House API')
    sys.exit(1)
