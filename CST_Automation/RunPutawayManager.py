#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import os
import re

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from putaway_automation import putaway_automation
from pendputaway_automation import pendputaway_automation
from login_automation import login_automation
from transfer_automation import transfer_automation

"""This script was written by Andrew Overton, January 2022."""

# Get current working directory (relative file path)
relative_path = os.getcwd()

# Initiate Chrome driver
s=Service(relative_path + '\chromedriver.exe')
driver = webdriver.Chrome(service=s)

# Run through the local login_automation module.
login_automation(s,driver)

# Ask for the pallet number and location the user wants to migrate the units towards.
check_pallet = True
while check_pallet == True:
    new_pallet = input("Pallet # (If you want to generate one, type 'generate'): ")
    if new_pallet.lower() == 'generate':
        generate_bool = True
        print("New pallet number will be generated.")
        check_pallet = False
    elif new_pallet == '':
        print("No input detected. Try Again. ")
    elif new_pallet.isnumeric() == True:
        generate_bool = False
        check_pallet = False
    else:
        print("Invalid Input. Try Again. ")
new_location = input('Pallet Location: ')

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
        print('Putaway status will not be shown.')
        report_input = False
    else:
        print('Invalid input. Try again.')
# Turn on or off "putaway" status updating.
update_input = True
while update_input == True:
    update_putaway_ask = input("Would you like to have the putaway status of units updated (yes/no)? ")
    update_putaway_ask = update_putaway_ask.lower()
    update_putaway = False
    if update_putaway_ask == 'yes':
        update_putaway = True
        print("Putaway status will be corrected.")
        update_input = False
    elif update_putaway_ask == 'no':
        print('Putaway status will not be corrected.')
        update_input = False
    else:
        print('Invalid input. Try again.')

print('Enter "quit" to continue to the next step or "remove" to delete the last entry')        
active_input = True
boxids_and_info=[]
# regular expression that, when used, removes everything but digits from the input string.
recompile = re.compile("[^\d]")
blank_dict = {'Box ID':'','Prev Pallet':'','New Pallet':'','Prev Location':'','New Location':'','Prev Status':'', 'New Status':''}
# Sort of convoluted way of making a new dictionary with the correct Box ID.
# Might be better to use classes, but I'm not familiar enough with them right now.
# Next iteration might use classes, though.
# UPDATE: Nevermind, the dictionaries work great I'm not changing them.
while active_input:
    boxid = input ('Box ID: ')
    if boxid.lower() == "quit":
        active_input = False
    elif boxid.lower() == "remove":
        del boxids_and_info[-1]
    else:
        # Make a copy of the blank dictionary and change the Box ID entry to the user input.
        # Automatically removes anything but numbers from boxid using the aforementioned regular expressions.
        new_dict = blank_dict.copy()
        new_dict['Box ID'] = recompile.sub('', boxid)
        boxids_and_info.append(new_dict)    

# Runs the local transfer_automation module.
transfer_automation(boxids_and_info, report_putaway, new_pallet, new_location, s, driver,generate_bool)

# Change status to putaway and update boxids_and_info with the new status.
if update_putaway == True:
    for dict_index in boxids_and_info:
        if dict_index['Prev Status'].lower() == 'putawayready':
            putaway_automation(dict_index['Box ID'],s,driver)
            dict_index['New Status'] = 'Putaway'
        elif dict_index['Prev Status'].lower() == 'pendputaway':
            pendputaway_automation(dict_index['Box ID'],new_pallet,new_location,s,driver)
            putaway_automation(dict_index['Box ID'],s,driver)
            dict_index['New Status'] = 'Putaway'
        else:
            pass

# Close Chrome instance.
driver.close()

# Get the date and time and add it to the beginning of the list of Box IDs and their info.
datetime_of_execution = time.asctime()
boxids_and_info.insert(0,{'Time Executed':datetime_of_execution})
# Append the list of units from this session to the text file specified
data_towards_csv = pd.DataFrame(boxids_and_info)
data_towards_csv.to_csv(relative_path + '\Reports\PutawayReference.txt', mode='a', index=None)
print('Finished. Report saved to ' + str(relative_path) + '\Reports\PutawayReference.txt')


# In[ ]:




