from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Ensure you provide the correct path to your chromedriver executable
service = Service(executable_path= "/Users/aravpant/Desktop/Projects/WebScraping/First-Project/chromedriver")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# Open Google
driver.get("https://fiber.google.com/db/")
df = pd.read_csv('/Users/aravpant/Desktop/Projects/WebScraping/AddressList/AddressWorking.csv')


for index,row in df.iterrows():
  address = row['address_primary']
  zip = row['zip']
  df['status'] = 'pending'

  elem = WebDriverWait(driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "input.address-checker__input.address-checker__input--street.borderable.pac-target-input"))
  )
  elem.clear()
  elem.send_keys(address)

  zipcode = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="hero-carousal"]/div[2]/div/div[1]/form/div/div[1]/div[3]/input'))
  )
  zipcode.clear()
  zipcode.send_keys(zip)
  zipcode.send_keys(Keys.RETURN)

  df['status'] = 'done'
  driver.get("https://fiber.google.com/db/")






time.sleep(10)
df.to_csv('/Users/aravpant/Desktop/Projects/WebScraping/AddressList/AddressWorking2.csv', index=False)
driver.quit()