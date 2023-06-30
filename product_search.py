from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import csv
import time
import re
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import argparse

def main():
	parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
	
	parser.add_argument('search_query',type=str)
	parser.add_argument('num', type=int)
	args = parser.parse_args()
 
	search_query = args.search_query
	driver = webdriver.Chrome()
	search_query = search_query.replace(" ", "%20")
	driver.get("https://www.carousell.sg/search/" + search_query)

	search_query = search_query.replace("%20", "_")
	csv_filename = search_query +".csv"
	csv_file = open(csv_filename, 'w', encoding='utf-8', newline='')
	writer = csv.writer(csv_file)

	index = 1

	while index <=args.num:
		try:
			print("Scraping chunk number " + str(index))
			index = index + 1

			# to find section of all listings 
			listings = driver.find_elements(By.XPATH, '//*[@id="main"]/div[2]/div/section[3]/div[1]/div/div')
			
			# listings = driver.find_elements(By.CSS_SELECTOR, "#main > div.D_e > div > section.D_q > div > div > div > div:nth-child(1) > div:nth-child(2) > div > div.D_xz") # 
			print(len(listings))
			
			# Iterate through the list and find the details of each review.
			listings_dict = {}
			for listing in listings:
				# Initialize an empty dictionary for each review
				listings_dict = {}

				description = ''
				try:
					product = listing.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/section[3]/div[1]/div/div/div[1]/div[' + str(index) + ']/div/div[1]/a[2]/p[1]')
					
				except:
					continue
				
				product = product.text
				
				price = listing.find_element(By.XPATH,'//*[@id="main"]/div[2]/div/section[3]/div[1]/div/div/div[1]/div['+ str(index) + ']/div/div[1]/a[2]/div[2]/p').text
				user = listing.find_element(By.XPATH,'//*[@id="main"]/div[2]/div/section[3]/div[1]/div/div/div[1]/div['+ str(index) + ']/div/div[1]/a[1]/div[2]/p').text
				#to scroll into view
				driver.execute_script("arguments[0].scrollIntoView();",listing)
				
				print('Product = {}'.format(product))
				print('Price = {}'.format(price))
				print('User = {}'.format(user))
				print('='*50)
				
				driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/section[3]/div[1]/div/div/div[1]/div[' + str(index) + ']/div').click()
				
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

				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[2]/div/section[3]/div[1]/div/div')))
					
				#driver.execute_script("arguments[0].scrollIntoView();",review)
				listings_dict['product'] = product
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
				pass #
				# writer.writerow(listings_dict.values())

		except Exception as e:
			print(e)
			csv_file.close()
			driver.close()
			break


if __name__ == "__main__":
	main()