from selenium import webdriver
from selenium.webdriver import ActionChains
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import username, password
import argparse

def main():
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argumnet('num', type=int)
    args = parser.parse_args()
	
    driver = webdriver.Chrome()

    driver.get("https://www.carousell.sg/likes/") 

    driver.find_element(By.XPATH, '//*[@id="ReactModalPortal-LOGIN"]/div/div/div/div/div[2]/button[2]').click()

    # Find the username/email field and send the username to the input field.
    uname = driver.find_element(By.XPATH, '//*[@id="ReactModalPortal-LOGIN"]/div/div/div/div/div[2]/form/div[1]/div/div/input')
    uname.send_keys(username)
    pword = driver.find_element(By.XPATH,'//*[@id="ReactModalPortal-LOGIN"]/div/div/div/div/div[2]/form/div[2]/div/div/input') 
    pword.send_keys(password)

    driver.find_element(By.XPATH, '//*[@id="ReactModalPortal-LOGIN"]/div/div/div/div/div[2]/form/button').click()

    # User has to complete CAPTCHA verification in browser UI

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[1]/div/div')))

    csv_filename = "my_likes.csv"
    csv_file = open(csv_filename, 'w', encoding='utf-8', newline='')
    writer = csv.writer(csv_file)

    index = 0
    time.sleep(2)
    # We want to start the first two pages.
    # If everything works, we will change it to while True
    while index <=args.num:
        try:
            index = index + 1
            print("Scraping chunk number " + str(index))
            
            listings = driver.find_elements(By.XPATH, '//*[@id="main"]/div[1]/div/div')
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[1]/div/div/div[' + str(index) + ']/div/div[1]')))
            time.sleep(2)
            # Iterate through the list and find the details of each review.
            listings_dict = {}
            for listing in listings:
                # Initialize an empty dictionary for each review
                listings_dict = {}
                description = ''
                    
                try:
                    # specific product section
                    product = listing.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div/div[' + str(index) + ']/div/div[1]')
                    
                except:
                    continue
            
                product_name = listing.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div/div[' + str(index) +']/div/div[1]/a[2]/p[1]').text
            
                price = listing.find_element(By.XPATH,'//*[@id="main"]/div[1]/div/div/div['+ str(index) + ']/div/div[1]/a[2]/div[2]/p').text
                user = listing.find_element(By.XPATH,'//*[@id="main"]/div[1]/div/div/div['+ str(index) + ']/div/div[1]/a[1]/div[2]/p').text
                
                # to scroll into view
                driver.execute_script("arguments[0].scrollIntoView();",listing)
                
                print('Product = {}'.format(product_name))
                print('Price = {}'.format(price))
                print('User = {}'.format(user))
                print('='*50)
                
                driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div/div[' + str(index) + ']/div/div[1]').click()
                
                try: 
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="FieldSetField-Container-field_description"]/div/div/div/div/p')))

                    description = driver.find_element(By.XPATH, '//*[@id="FieldSetField-Container-field_description"]/div/div/div/div/p')
                except:
                    pass
                description_text = ''
                if description is not None:
                    if isinstance(description, str):
                        description_text = description
                    else: 
                        description_text = description.text
                        description_text = description_text.replace("\n", " ")
             
                print("Description:",description_text)
                time.sleep(2)
                driver.back()
        
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[1]/div/div')))
                        
                #driver.execute_script("arguments[0].scrollIntoView();",review)
                listings_dict['product'] = product_name
                listings_dict['price'] = price 
                listings_dict['user'] = user
                listings_dict['description'] =description_text
        

                writer.writerow(listings_dict.values())
                
            # We need to scroll to the bottom of the page because the button is not in the current view yet.
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #time.sleep(1)
            # Locate the next button element on the page and then call `button.click()` to click it.
            try:
                button = driver.find_element(By.XPATH,'//button[@class="styles__button___3dxOP desktop__button___2Hl0n styles__medium___3KEDn styles__outline___3AGrh desktop__outline___2UF39 styles__loadMore___yYAF4"]')
                #time.sleep(1)
                actions = ActionChains(driver)
                actions.move_to_element(button).click().perform()

                time.sleep(1)

            except:
                pass
            
        except Exception as e:
            print(e)
            csv_file.close()
            driver.close()
            break


if __name__ == "__main__":
	main()