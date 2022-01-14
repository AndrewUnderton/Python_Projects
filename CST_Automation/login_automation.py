#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import getpass

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""This script was written by Andrew Overton, January 2022."""


def login_automation(s, driver):
    """Take input from user and Chrome driver from main script. Attempt to login to CST with that information."""
    cst_login_url = "https://w16kcst2.int.hp.com/"

    # Keep asking for login until it works.
    need_login = True
    while need_login == True:
        # Ask user for login information, keep password secret not plaintext.
        email = input('Email for CST: ')
        password = getpass.getpass('Password: ')
        # open the login screen for CST
        driver.get(cst_login_url)
        # Find the CSS text fields and button for inputing login information
        find_email = driver.find_element(By.XPATH, '//*[@id="Email"]')
        find_password = driver.find_element(By.XPATH, '//*[@id="Password"]')
        find_login = driver.find_element(By.XPATH, '/html/body/section[2]/div/div[1]/div/div/div[1]/form/div[4]/button')
        # Input login info that user input earlier and click the login button
        find_email.send_keys(email);
        find_password.send_keys(password);
        find_login.click();
        # If Chrome doesn't go to the change log screen after trying to log in, that means it failed, so try again.
        try:
            WebDriverWait(driver, 6).until(EC.url_to_be('https://w16kcst2.int.hp.com/ChangeLog'))
            need_login == False
            print('Login successful!')
            break
        except TimeoutException:
            print('Login was incorrect, please try again.')

