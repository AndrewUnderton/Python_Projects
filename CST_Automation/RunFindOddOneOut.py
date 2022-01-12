#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import os
import re

import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from login_automation import login_automation

# This program is to find, alert of, and update any units which are not in the pallet that have been listed.
# Enter the correct pallet # and location, and any that don't match that pallet # will be highlighted for you.
# It was built off of an earlier version of the transfer_automation module with slightly different utilization.

relative_path = os.getcwd()

# URL of CST Transfer Manager as of 1/04/2022
transfer_url = 'https://w16kcst2.int.hp.com/Warehouse/StockTransfer'
boxid_url_prefix = '?boxID='
boxid_trans_url_prefix = '?page=1&boxID='
boxid_trans_url_suffix = '&transferID='

# Ask for the pallet and location that the units will change to. In future iterations
# You'll be able to put in a list of all the pallets and then the program will assign
# automatically based on the part number.
new_pallet = input('Pallet #: ')
new_location = input('Pallet Location: ')

print('Enter "quit" to continue to the next step or "remove" to delete the last entry')        
active_input = True
boxids_and_info=[]
# regular expression that, when used, removes everything but digits from the input string.
recompile = re.compile("[^\d]")
blank_dict = {'Box ID':'','Prev Pallet':'','New Pallet':'','Prev Location':'','New Location':'','Status':''}
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
        # Automatically removes anything but numbers from boxid using the aforementioned regular expressions.
        new_dict = blank_dict.copy()
        new_dict['Box ID'] = recompile.sub('', boxid)
        boxids_and_info.append(new_dict)   

#print(boxids_and_info)

s=Service(relative_path + '\chromedriver.exe')
driver = webdriver.Chrome(service=s)

login_automation(s,driver)

# Loop through all the Box ID's the user input
for dict_index in boxids_and_info:
    grab_id = dict_index['Box ID']
    
    # Create the URL for the Transfer Manager for that specific Box ID and go to that address.
    boxid_url = transfer_url + boxid_url_prefix + grab_id
    url_for_load_wait = transfer_url + boxid_trans_url_prefix + grab_id + boxid_trans_url_suffix + grab_id
    driver.get(boxid_url)
    
    # Find the CSS and save the info for before the pallet and location update.
    unit_status = driver.find_element(By.XPATH,'/html/body/section[2]/div/div[2]/div/div/div/table/tbody/tr/td[6]').text
    unit_pallet = driver.find_element(By.XPATH,'/html/body/section[2]/div/div[2]/div/div/div/table/tbody/tr/td[7]').text
    unit_location = driver.find_element(By.XPATH,'/html/body/section[2]/div/div[2]/div/div/div/table/tbody/tr/td[9]').text
    dict_index['Status'] = unit_status
    dict_index['Prev Pallet'] = unit_pallet
    dict_index['Prev Location'] = unit_location
    
    if unit_pallet == new_pallet:
        continue
    else:
        input("Found one that doensn't match! Its Box ID is: " + grab_id + " press ENTER to fix it and continue looking. ")
        # Find the CSS button to open the options for this unit, and click the button
        find_next = driver.find_element(By.XPATH,'/html/body/section[2]/div/div[2]/div/div/div/table/tbody/tr/td[1]/div/a[1]')
        find_next.click()
        time.sleep(.5)

        # Find the CSS text fields and button for filling out new information
        find_pallet = driver.find_element(By.ID,'txtPalletID')
        find_location = driver.find_element(By.ID,'TransferPart_MDM_Location_LocationNumber')
        find_save = driver.find_element(By.ID,'btnConfirmYes')

        # Fill in the found locations and click the save button
        find_pallet.clear()
        find_pallet.send_keys(new_pallet)
        find_location.clear()
        find_location.send_keys(new_location)
        find_save.click()
        # Wait til the new information saves (or time out after 60 seconds)
        try:
            WebDriverWait(driver, 60).until(EC.url_to_be('https://w16kcst2.int.hp.com/Warehouse/StockTransfer?firstload=true'))
        except:
            print("This has taken to long")
            input("Press ENTER to continue once the page has loaded (or quit and restart from " + grab_id + "): ")
        dict_index['New Pallet'] = new_pallet
        dict_index['New Location'] = new_location
        
# Get the date and time and add it to the beginning of the list of Box IDs and their info.
datetime_of_execution = time.asctime()
boxids_and_info.insert(0,{'Time Executed':datetime_of_execution})
# Append the list of units from this session to the text file specified
data_towards_csv = pd.DataFrame(boxids_and_info)
data_towards_csv.to_csv(relative_path + '\Reports\OddOneOutReference.txt', mode='a', index=None)
print('Finished. Report saved to ' + str(relative_path) + '\Reports\OddOneOutReference.txt')
driver.close()


# In[ ]:




