#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import os

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from itertools import islice

from login_automation import login_automation

# Get current working directory (relative file path)
relative_path = os.getcwd()

# Read the BoxIDs from the excel file being used and convert to an easy-to-read list.
# UPDATE: These three lines are no longer necessary because IDs are now grabbed 
# directly from Transfer Manager.
# Also, Excel decided I needed an account after 1 month so I had to turn this part off.
#print_table = pd.read_excel(relative_path + '\Reports\PyPrintReference.xlsx')
#print_table = print_table.fillna("")
#print_list = print_table['BoxIDs'].tolist()

# Create a new instance of Chrome to utilize.
s=Service(relative_path + '\chromedriver.exe')
driver = webdriver.Chrome(service=s)

# Run through the local login_automation module.
login_automation(s,driver)
 
# Go to the Transfer Manager page for the inputted pallet number.
transfer_url = 'https://w16kcst2.int.hp.com/Warehouse/StockTransfer?boxID=&pallet=' + str(pallet_number)
driver.get(transfer_url)
more_page = True
current_page = 1
box_ids = []

# Grab all the Box IDs saved to the pallet number in Transfer Manager.
while more_page == True:
    print('Currently reading page ' + str(current_page))
    # Find the total number of rows in the table of Box IDs in Transfer Manager.
    total_rows = driver.find_elements(By.XPATH, '/html/body/section[2]/div/div[2]/div/div/div/table/tbody/tr')
    total_rows = len(total_rows)
    # In each row, grab the second element (the Box ID) and save it to the list of Box IDs
    for elem in range(total_rows):
        row_num = str(elem+1)
        add_boxid = driver.find_element(By.XPATH, '/html/body/section[2]/div/div[2]/div/div/div/table/tbody/tr[' + row_num + ']/td[2]').text
        box_ids.append(add_boxid)
    # If the "next page" button exists and is clickable (wait a little while to make sure it's clickable),
    # click it so we can get the next set of Box IDs. Otherwise stop the loop.
    try:
        next_page = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "PagedList-skipToNext")))
        next_page.click()
        current_page += 1
    except (TimeoutException,NoSuchElementException):
        more_page = False
        print("No more pages!")

# Set the number of labels needed to the total amount of Box IDs.
num = len(box_ids)
num_done = 0

while num != num_done:
    # When there are 50 or more labels needed, only print 50 at a time.
    if num-num_done >= 50:
        # interate over the list of BoxIDs, starting at what's been done already, to 50 after that.
        for i in islice(box_ids, num_done, (num_done+50)):
            # if the BoxID is blank, don't do anything
            if i == "" or i == "nan":
                continue
            # if there is a BoxID, go to the Inventory Lookup page of that item
            else:
                print(i)
                lookup_url = "https://w16kcst2.int.hp.com/Warehouse/Lookup?BoxID=" + str(int(i))
                driver.get(lookup_url)
                # Find the printer button and click it
                printer = driver.find_element(By.TITLE, 'Print Label')
                printer.click()
                # There is a second prompt afterwards that confirms if you want to print. Click yes.
                printer_ok = driver.find_element(By.ID, "btnPrintBox")
                printer_ok.click()
        num_done = num_done + 50
    # When there are less than 50 labels needed, only print that many.
    elif num-num_done >= 0 and num-num_done < 50:
        # interate over the list of BoxIDs
        for i in islice(box_ids, num_done, (num_done+(num-num_done))):
            # if the BoxID is blank, don't do anything
            if i == "" or i == "nan":
                continue
            # if there is a BoxID, go to the Inventory Lookup page of that item
            else:
                print(i)
                lookup_url = "https://w16kcst2.int.hp.com/Warehouse/Lookup?BoxID=" + str(int(i))
                driver.get(lookup_url)
                # Find the printer button and click it
                printer = driver.find_element(By.TITLE,'Print Label')
                printer.click()
                # There is a second prompt afterwards that confirms if you want to print. Click yes.
                printer_ok = driver.find_element(By.ID, "btnPrintBox")
                printer_ok.click()
        num_done = num_done + (num-num_done)
    else:
        pass
    # Check if there are more labels to be printed and let the user know how many have been printed thus far.
    if num_done != num:
        input(str(num_done) + " labels have been printed so far.\nThere are " + str(num-num_done) + " labels left to print.\nPress ENTER to continue to the next batch. ")
    else:
        pass
        
# close webpage and alert user that the script has finished.
driver.close()
print('Finished.')


# In[ ]:




