from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import csv
import time
import re
from selenium.webdriver.common.by import By
import pandas as pd

search_query = "fresh samples" # change this
driver = webdriver.Chrome()

# Launch the browser and open the github URL in your web driver.
driver.get("https://www.carousell.sg/login")

driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/button[2]").click() 
# driver.find_element("title", "Email, username or mobile").click() 

# Find the username/email field and send the username to the input field.
uname = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div[2]/div[1]/form/div[1]/div/div/input') 
uname.send_keys("wayyymayyyy")

# Find the password input field and send the password to the input field.
pword = driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[2]/div/div[2]/div[1]/form/div[2]/div/div/input') 
pword.send_keys("Carousell987!")

# Click sign in button to login the website.
driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div[2]/div[1]/form/button').click()
# Wait for login process to complete. 
# driver.WebDriverWait(driver=driver, timeout=10).until(
#     lambda x: x.execute_script("return document.readyState === 'complete'")
# )
# # Verify that the login was successful.
# error_message = "Incorrect username or password."
# # Retrieve any errors found. 
# errors = driver.find_elements(By.CLASS_NAME, "flash-error")

# # When errors are found, the login will fail. 
# if any(error_message in e.text for e in errors): 
#     print("[!] Login failed")
# else:
#     print("[+] Login successful")
# # Close the driver
# driver.close()

# go to my likes page
driver.get("https://www.carousell.sg/likes/")
