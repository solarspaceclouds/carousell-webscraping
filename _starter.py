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

search_query = "fresh samples" # change this
driver = webdriver.Chrome()
search_query = search_query.replace(" ", "%20")
driver.get("https://www.carousell.sg/search/" + search_query)
#?slt=null

# Click review button to go to the review section
#category_button = driver.find_element_by_xpath('//span[@class="padLeft6 cursorPointer"]')
#category_button.click()

#category_urls = driver.find_elements_by_xpath('//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div[1]/div/a/@href')
search_query = search_query.replace("%20", "_")
csv_filename = search_query +".csv"
csv_file = open(csv_filename, 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

# time.sleep(3)
# property_button = driver.find_element(By.XPATH,'//div[2]/a[@class="styles__collectionLink___37_IC styles__link___9msaS"]')
# property_button.click()
# time.sleep(3)

index = 1
# We want to start the first two pages.
# If everything works, we will change it to while True
while index <=16:
	try:
		print("Scraping chunk number " + str(index))
		index = index + 1
		# Find all the reviews. The find_elements function will return a list of selenium select elements.
		# Check the documentation here: http://selenium-python.readthedocs.io/locating-elements.html
		# listings = driver.find_element(By.XPATH,'//div[@class="styles__cardContent___TpQXu"]')
		# listings = driver.find_elements(By.CLASS_NAME, "D_xz")
		listings = driver.find_elements(By.XPATH, '//*[@id="main"]/div[1]/div/section[3]/div/div')
		# listings = driver.find_elements(By.CSS_SELECTOR, "#main > div.D_e > div > section.D_q > div > div > div > div:nth-child(1) > div:nth-child(2) > div > div.D_xz") # 
		print(len(listings))
		
		# Iterate through the list and find the details of each review.
		listings_dict = {}
		for listing in listings:
			# Initialize an empty dictionary for each review
			listings_dict = {}
			# Use try and except to skip the review elements that are empty. 
			# Use relative xpath to locate the title.
			# Once you locate the element, you can use 'element.text' to return its string.
			# To get the attribute instead of the text of each element, use 'element.get_attribute(href) for example'
			description = ''
			try:
				# <p class="D_rE D_qk D_rF D_rJ D_rL D_rP D_rS D_rV" data-testid="listing-card-text-seller-name">carly57</p>
				# //*[@id="main"]/div[1]/div/section[3]/div/div/div/div[1]/div[1]/div
				product = listing.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/section[3]/div/div/div/div[1]/div[' + str(index) + ']/div/div[1]/a[2]/p[1]')
				# product = listing.find_element(By.XPATH, "//*[@id='main']/div[1]/div/section[3]/div/div/div/div[1]/div[1]/div/div[1]/a[2]/p[3]")
				# product = listing.find_element(By.CLASS_NAME, 'D_xy')
				# product = listing.find_elements(By.CSS_SELECTOR, "> a.D_xE.D_tN > div.D_xH > p").text
				
				
				
			except:
				continue
			
			product = product.text
			price = listing.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/main/div[1]/div/section[3]/div/div/div/div[1]/div['+ str(index) + ']/div/div[1]/a[2]/div[2]/p').text
			user = listing.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div/main/div[1]/div/section[3]/div/div/div/div[1]/div['+ str(index) + ']/div/div[1]/a[1]/div[2]/p').text
			#to scroll into view
			driver.execute_script("arguments[0].scrollIntoView();",listing)
			
			print('Product = {}'.format(product))
			print('Price = {}'.format(price))
			print('User = {}'.format(user))
			print('='*50)
			
			driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/section[3]/div/div/div/div[1]/div[' + str(index) + ']/div/div[1]').click()
			
				# delay = 3 # seconds
				# try:
				# 	myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
				# 	print "Page is ready!"
				# except TimeoutException:
				# 	print "Loading took too much time!"
				# driver.explicitly_wait(6)
			# enter product page
			# //*[@id="main"]/div[1]/div/section[3]/div/div/div/div[1]/div[8]/div/div[1]/a[2]/p[1]
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="FieldSetField-Container-field_description"]/div/div/div/div/p')))
				
			description = driver.find_element(By.XPATH, '//*[@id="FieldSetField-Container-field_description"]/div/div/div/div/p')
			if description is not None:
				description_text = description.text
		
			else:
				description_text = ''
			print("Description:",description_text)
			driver.back()
			# WebDriverWait(driver, 10).until(By.XPATH, '//*[@id="main"]/div[1]/div/section[3]/div/div/div/div[1]/div[' + str(index) + ']/div/div[1]/a[2]/p[1]')

			

			
			# Use relative xpath to locate text, username, date_published, rating.
			# Your code here

			# Uncomment the following lines once you verified the xpath of different fields
			#text = review.find_element_by_xpath('.//span[@class = "pad6 onlyRightPad"]').text
			#rating = review.find_element_by_xpath('//*[@id="reviews"]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/span/span[3]/span[1]').text
			
			#driver.execute_script("arguments[0].scrollIntoView();",review)
			listings_dict['product'] = product
			listings_dict['price'] = price 
			listings_dict['user'] = user
			listings_dict['description'] =description_text
			# review_dict['date_published'] = date_published
			#review_dict['rating'] = rating

			writer.writerow(listings_dict.values())
			
			#print('Text={}'.format(text))
			#print('Rating={}'.format(rating))

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

# print(pd.read_csv(csv_file))
with open(csv_filename, 'a+') as file:
    print(file.readlines())
 