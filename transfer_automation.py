#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def transfer_automation(boxids_and_info,report_putaway,new_pallet,new_location,s,driver,generate_bool):
    """Take the list of dictionaries of units from the main script,
       transfer the units to the correct pallets and locations,
       and then save the new information for saving to the report.
       """
    # Base parts of the URL for CST Transfer Manager as of Jan 07, 2022.
    transfer_url = 'https://w16kcst2.int.hp.com/Warehouse/StockTransfer'
    boxid_url_prefix = '?boxID='
    boxid_trans_url_prefix = '?page=1&boxID='
    boxid_trans_url_suffix = '&transferID='
    print_gen = False
    
    for dict_index in boxids_and_info:
        grab_id = dict_index['Box ID']

        # Combine the URL parts and Box ID into a full URL to access Transfer Manager and go to that link.
        boxid_url = transfer_url + boxid_url_prefix + grab_id
        url_for_load_wait = transfer_url + boxid_trans_url_prefix + grab_id + boxid_trans_url_suffix + grab_id
        driver.get(boxid_url)

        # Find the CSS and save the info of where the unit was located before the transfer.
        unit_status = driver.find_element(By.XPATH, '/html/body/section[2]/div/div[2]/div/div/div/table/tbody/tr/td[6]').text
        unit_pallet = driver.find_element(By.XPATH, '/html/body/section[2]/div/div[2]/div/div/div/table/tbody/tr/td[7]').text
        unit_location = driver.find_element(By.XPATH, '/html/body/section[2]/div/div[2]/div/div/div/table/tbody/tr/td[9]').text
        dict_index['Prev Status'] = unit_status
        dict_index['Prev Pallet'] = unit_pallet
        dict_index['Prev Location'] = unit_location
        
        # Alert the user of the putaway status of the unit.
        if report_putaway == True:
            if unit_status.lower() == 'pendputaway':
                print('Unit ' + grab_id + ' is currently Pending Putaway.')
            elif unit_status.lower() == 'putawayready':
                print('Unit ' + grab_id + ' is currently Putaway Ready.')
            elif unit_status.lower() == 'putaway':
                print('Unit ' + grab_id + ' is currently Putaway. No input needed.')
            else:
                print('Unit ' + grab_id + ' is currently ' + unit_status.lower() + '.')
        else:
            pass

        if generate_bool == True:
            # Find the CSS button to open the options for this unit, and click the button
            find_next = driver.find_element(By.XPATH, '/html/body/section[2]/div/div[2]/div/div/div/table/tbody/tr/td[1]/div/a[1]')
            find_next.click()
            #Generate a new pallet number
            find_generate = driver.find_element(By.ID, 'cmdGenerate')
            find_generate.click()
            # Find the CSS text fields and button for filling out new information
            find_location = driver.find_element(By.ID, 'TransferPart_MDM_Location_LocationNumber')
            find_save = driver.find_element(By.ID, 'btnConfirmYes')
            # Read the generated pallet number, fill in the location, and click save.
            pallet_box = driver.find_element(By.ID, 'txtPalletID')
            gen_pallet = pallet_box.get_property("value")
            find_location.clear()
            find_location.send_keys(new_location)
            find_save.click()
            # Wait til the new information saves (or time out after 60 seconds)
            try:
                WebDriverWait(driver, 60).until(EC.url_to_be('https://w16kcst2.int.hp.com/Warehouse/StockTransfer?firstload=true'))
            except:
                print("This has taken to long")
                input("Press ENTER to continue once the page has loaded (or quit and restart from " + grab_id + "): ")
            # Save the new locations in the dictionary entry for this unit.
            dict_index['New Pallet'] = gen_pallet
            dict_index['New Location'] = new_location
            generate_bool = False
            print_gen = True
            new_pallet = gen_pallet
        elif unit_pallet != new_pallet or unit_location != new_location:
            # Find the CSS button to open the options for this unit, and click the button
            find_next = driver.find_element(By.XPATH, '/html/body/section[2]/div/div[2]/div/div/div/table/tbody/tr/td[1]/div/a[1]')
            find_next.click()
            # Find the CSS text fields and button for filling out new information
            find_pallet = driver.find_element(By.ID, 'txtPalletID')
            find_location = driver.find_element(By.ID, 'TransferPart_MDM_Location_LocationNumber')
            find_save = driver.find_element(By.ID, 'btnConfirmYes')
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
            # Save the new locations in the dictionary entry for this unit.
            dict_index['New Pallet'] = new_pallet
            dict_index['New Location'] = new_location
        else:
            pass
    if print_gen == True:
        print("The generated pallet number is " + gen_pallet + ".")

