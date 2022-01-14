#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""This script was written by Andrew Overton, January 2022."""


def pendputaway_automation(boxid,new_pallet,new_location,s,driver):
    """Handles the Putaway Receiving portion of putting a unit away. Specifically Pendputaway status."""
    # Make the Pendputaway URL and go to it.
    pend_url_prefix = ('https://w16kcst2.int.hp.com/Rec/Putaway?status=7&projectID=&boxID=')
    pend_url = pend_url_prefix + str(boxid)
    driver.get(pend_url)
    
    settings_button = driver.find_element(By.CLASS_NAME, 'mdi-pencil-outline')
    settings_button.click()
    # Find the textboxes for filling in location and pallet as well as the save button.
    location_field = driver.find_element(By.ID, 'SingleEdit_MDM_Location_LocationNumber')
    pallet_field = driver.find_element(By.ID, 'txtPalletID')
    save_button = driver.find_element(By.ID, 'btnSavePendPutaway')
    # Fill in the textboxes and save the information.
    location_field.clear()
    location_field.send_keys(new_location)
    pallet_field.clear()
    pallet_field.send_keys(new_pallet)
    save_button.click()
    # Wait til the new information saves (or time out after 60 seconds)
    try:
        WebDriverWait(driver, 60).until(EC.url_to_be('https://w16kcst2.int.hp.com/Rec/Putaway?firstload=True'))
    except:
        print("This has taken to long. Internet might be down.")
        input("Press ENTER to continue once the page has loaded (or quit and restart from " + grab_id + "): ")

