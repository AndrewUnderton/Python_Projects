#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def putaway_automation(boxid, s, driver):
    """Take the Box IDs which are given by the user in the main scripts, and put the units into Putaway status."""
    ardt_url = 'https://w16kcst2.int.hp.com/ARDT/Putaway?boxID='
    suffix = '&EditID='
    putaway_url = ardt_url + str(boxid) + suffix + str(boxid)
    driver.get(putaway_url)
    # Show the common condition codes for ARDT and let the user select from the options.
    ddelement = Select(driver.find_element(By.NAME, 'FK_INV_ConditionCodes'))
    valid_condition = False
    while valid_condition == False:
        condition = input('Please select a condition code for unit ' + str(boxid) + ' (A/B/C/D)').upper()
        if condition == 'A':
            ddelement.select_by_visible_text('A - Like New')
            valid_condition = True
        elif condition == 'B':
            ddelement.select_by_visible_text('B - Some Cosmetic Flaws')
            valid_condition = True
        elif condition == 'C':
            ddelement.select_by_visible_text('C - Requires Repair')
            valid_condition = True
        elif condition == 'D':
            ddelement.select_by_visible_text('D - Broken/No Value')
            valid_condition = True
        else:
            print('Invalid Input. Try again.')
    # Show the common encryption status for ARDT and let the user select from the options.
    ddelement = Select(driver.find_element(By.NAME, 'FK_INV_EncryptionStatus'))
    valid_condition = False
    while valid_condition == False:
        condition = input('Please select an encryption status for unit ' + str(boxid) + '\n([1]Encrypted, [2]No Drive, [3]Not Encrypted, [4]Unknown, [5]Wiped)').lower()
        if condition == 'encrypted' or condition == '1' or condition == '[1]encrypted':
            ddelement.select_by_visible_text('Encrypted')
            valid_condition = True
        elif condition == 'no drive' or condition == '2' or condition == '[2]no drive':
            ddelement.select_by_visible_text('No Drive Present')
            valid_condition = True
        elif condition == 'not encrypted' or condition == '3' or condition == '[3]not encrypted':
            ddelement.select_by_visible_text('Not Encrypted')
            valid_condition = True
        elif condition == 'unknown' or condition == '4' or condition == '[4]unknown':
            ddelement.select_by_visible_text('Unknown')
            valid_condition = True
        elif condition == 'wiped' or condition == '5' or condition == '[5]wiped':
            ddelement.select_by_visible_text('Wiped')
            valid_condition = True
        else:
            print('Invalid Input. Try again.')
    # Look through all the options for memory size in the drop-down list, show the user all the available options, and await input.
    valid_memory = False
    while valid_memory == False:
        memories = []            
        ddelement = Select(driver.find_element(By.NAME, 'FK_INV_Memory'))
        print('The following are the available options for the memory of unit ' + boxid + ':')
        for options in ddelement.options:
            print(options.text)
            memories.append(options.text)
        memory_input = input("Please select one of the options. If the option isn't present, type REFRESH")
        if memory_input.lower() == 'refresh':
            input('Please go to Project Part Admin and add the appropriate memory. Press ENTER when complete: ')
            valid_condition = True 
            driver.get(putaway_url)
        elif memory_input in memories:
            ddelement.select_by_visible_text(memory_input)
            valid_memory = True
        else:
            print('Invalid Input. Try again.')
    
    # Look through all the options for drive size in the drop-down list, show the user all the available options, and await input.
    valid_drive = False
    while valid_drive == False:
        harddrives = []            
        ddelement = Select(driver.find_element(By.NAME, 'FK_INV_HardDisk'))
        print('The following are the available options for the Hard Disk of unit ' + boxid + ':')
        for options in ddelement.options:
            print(options.text)
            harddrives.append(options.text)
        drive_input = input("Please select one of the options. If the option isn't present, type REFRESH ")
        if drive_input.lower() == 'refresh':
            input('Please go to Project Part Admin and add the appropriate memory. Press ENTER when complete: ')
            valid_condition = True 
            driver.get(putaway_url)
        elif drive_input in harddrives:
            ddelement.select_by_visible_text(drive_input)
            valid_drive = True
        else:
            print('Invalid Input. Try again.')
    # Save all the previously inputted information.
    save_putaway = driver.find_element(By.ID, 'btnSavePendPutaway')
    save_putaway.click()
    # Wait for the save to finish before going to the next unit.
    try:
        WebDriverWait(driver, 60).until(EC.url_to_be('https://w16kcst2.int.hp.com/ARDT/Putaway?boxID=' + boxid))
    except:
        print("This is taking too long.")
        input("Press ENTER once status has finished saving.")

