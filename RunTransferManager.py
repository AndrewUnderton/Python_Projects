#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import os
import re

import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from login_automation import login_automation
from transfer_automation import transfer_automation


# Get current working directory (relative file path)
relative_path = os.getcwd()

# Run through the local login_automation module.
login_automation(s,driver)

# Ask for the pallet number and location the user wants to migrate the units towards.
new_pallet = input("Pallet # (If you want to generate one, type 'generate'): ")
new_location = input('Pallet Location: ')

if new_pallet.lower() == 'generate':
    generate_bool = True
    print("New pallet number will be generated.")
else:
    generate_bool = False
    pass

# Turn on or off "putaway" status reporting.
report_input = True
while report_input == True:
    report_putaway_ask = input("Would you like to have the putaway status of units reported (yes/no)? ")
    report_putaway_ask = report_putaway_ask.lower()
    report_putaway = False
    if report_putaway_ask == 'yes':
        report_putaway = True
        print("Putaway status will be shown.")
        report_input = False
    elif report_putaway_ask == 'no':
        print('Putaway status will not be shown or corrected.')
        report_input = False
    else:
        print('Invalid input, try again.')

print('Enter "quit" to continue to the next step or "remove" to delete the last entry')        
active_input = True
boxids_and_info=[]
# Regular expression that, when used, removes everything but digits from the input string.
recompile = re.compile("[^\d]")
blank_dict = {'Box ID':'','Prev Pallet':'','New Pallet':'','Prev Location':'','New Location':'','Prev Status':'', 'New Status':''}
# Sort of convoluted way of making a new dictionary with the correct Box ID. Would be better
# to use classes I believe, but I'm not familiar enough with them right now.
# Next iteration might use classes, though.
# UPDATE: Nevermind, the dictionaries work great I'm not changing them.
while active_input:
    boxid = input ('Box ID: ')
    if boxid.lower() == "quit":
        active_input = False
    elif boxid.lower() == "remove":
        del boxids_and_info[-1]
    else:
        # Make a copy of the blank dictionary and change the box id entry to the user input.
        # Automatically removes anything but numbers from boxid using regular expressions.
        new_dict = blank_dict.copy()
        new_dict['Box ID'] = recompile.sub('', boxid)
        boxids_and_info.append(new_dict)    

# open the login screen for CST
s=Service(relative_path + '\chromedriver.exe')
driver = webdriver.Chrome(service=s)

# Run through the local transfer_automationmodule.
transfer_automation(boxids_and_info,report_putaway,new_pallet,new_location,s,driver)
# Close the Chrome Instance
driver.close()

# Get the date and time and add it to the beginning of the list of Box IDs and their info.
datetime_of_execution = time.asctime()
boxids_and_info.insert(0,{'Time Executed':datetime_of_execution})
# Append the list of units from this session to the text file specified
data_towards_csv = pd.DataFrame(boxids_and_info)
data_towards_csv.to_csv(relative_path + '\Reports\TransferReference.txt', mode='a', index=None)

print('Finished. Report saved to ' + str(relative_path) + '\Reports\TransferReference.txt')


# In[ ]:




