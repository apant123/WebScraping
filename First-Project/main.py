from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Ensure you provide the correct path to your chromedriver executable
service = Service(executable_path= "/Users/aravpant/Desktop/Projects/WebScraping/First-Project/chromedriver")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# Open Google
driver.get("https://orteil.dashnet.org/cookieclicker/")


cookie_id = "bigCookie"
cookies_id = "cookies"
product_price_prefix = "productPrice"
product_prefix = "product"


WebDriverWait(driver, 20).until(
  EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]"))
)

language = driver.find_element(By.XPATH, "//*[contains(text(), 'English')]")
language.click()


WebDriverWait(driver, 5).until(
  EC.presence_of_element_located((By.ID, cookie_id))
)



cookie = driver.find_element(By.ID, cookie_id)



while True:
  cookie.click()
  cookies_count = driver.find_element(By.ID, cookies_id).text.split(" ")[0]
  cookies_count = int(cookies_count.replace(",", ""))
  print(cookies_count)

  for i in range(4):
    product_price = driver.find_element(By.ID, product_price_prefix + str(i)).text.replace(",", "")

    if not product_price.isdigit():
      continue

    product_price = int(product_price)

    if cookies_count >= product_price:
      product = driver.find_element(By.ID, product_prefix  + str(i))
      product.click()
      break



driver.quit()

# WebDriverWait(driver, 5).until(
#   EC.presence_of_element_located((By.CLASS_NAME,"gLFyf"))
# )

# input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
# input_element.clear()
# input_element.send_keys("arav pant" + Keys.ENTER)

# WebDriverWait(driver, 5).until(
#   EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Arav Pant - UCLA - Los Angeles, California, United States"))
# )


# link = driver.find_element(By.PARTIAL_LINK_TEXT, "Arav Pant - UCLA - Los Angeles, California, United States")
# link.click()


# time.sleep(10)

# # Close the browser
# driver.quit()
