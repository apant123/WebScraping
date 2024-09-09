from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import time




start_time = time.time()
# Ensure you provide the correct path to your chromedriver executable
service = Service(executable_path= "/Users/aravpant/Desktop/Projects/WebScraping/First-Project/chromedriver")

#Add Chrome Options
chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920,1080')
# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
# Open Google
pricing = False
driver.get("https://fiber.google.com/db/")
df = pd.read_csv('/Users/aravpant/Desktop/Projects/WebScraping/AddressList/small.csv')
csvpath = '/Users/aravpant/Desktop/Projects/WebScraping/AddressList/ad4.csv'

def check_element(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        # elem = WebDriverWait(driver, 2).until(
        # EC.presence_of_element_located((By.XPATH, xpath))
        # )
        return True
    except:
        return False
        

def find_price(driver,xpath, timeout):
    try:
      # element = driver.find_element(By.XPATH,xpath)
      element = WebDriverWait(driver, timeout).until(
          EC.presence_of_element_located((By.XPATH, xpath))
      )
      return [True,element.text]
    except:
       return [False, "Null"]

for index,row in df.iterrows():
  address = row['address_primary']
  zip = row['zip']
  #df['1_Gig'] = 'default_value'
  #df.at[index, 'status'] = 'pending'
  #df.to_csv(csvpath, index=False)
  elem = WebDriverWait(driver, 100).until(
          EC.presence_of_element_located((By.XPATH, '//*[@id="hero-carousal"]/div[2]/div/div[1]/form/div/div[1]/div[1]/div/input'))
  )
  elem.clear()
  elem.send_keys(address)

  zipcode = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="hero-carousal"]/div[2]/div/div[1]/form/div/div[1]/div[3]/input'))
  )

  zipcode.clear()
  zipcode.send_keys(zip)
  zipcode.send_keys(Keys.RETURN)
  #time.sleep(1)
  try:
    element = WebDriverWait(driver, 10).until(
        EC.any_of(
            EC.presence_of_element_located((By.XPATH, '/html/body/modularsignup-app/sequence/div[1]/main/div/div/base-step/section/preconfig-step/div/preconfig-card/div')),  # Eligible
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/address-app/div/cta-view/cta-container/cta-mailing/div/div/div[1]/div/h1')),  # Unavailable
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/address-app/div/cta-view/cta-container/cta-already-registered/div/h1')),  # Has Account
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/address-app/div/cta-view/address-search/button/span[2]')),  # Need Apt
            EC.presence_of_element_located((By.XPATH, '//*[@id="mat-radio-2-input"]'))  # Business
        )
    )
  except TimeoutException:
     df.at[index, 'status'] = 'Something'

  if check_element(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div/div/base-step/section/preconfig-step/div/preconfig-card/div'):
    df.at[index, 'status'] = 'Eligible'
    pricing = True
  elif check_element(driver, '/html/body/div[1]/address-app/div/cta-view/cta-container/cta-mailing/div/div/div[1]/div/h1'):
    df.at[index, 'status'] = 'Unavailable'
  elif check_element(driver, '/html/body/div[1]/address-app/div/cta-view/cta-container/cta-already-registered/div/h1'):
    df.at[index, 'status'] = 'Has Account'
  elif check_element(driver, '/html/body/div[1]/address-app/div/cta-view/address-search/button/span[2]'):
    df.at[index, 'status'] = 'Need Apt'
  elif check_element(driver, '//*[@id="mat-radio-2-input"]'):
     df.at[index, 'status'] = 'Business'
  else:
    df.at[index, 'status'] = 'Something'

  if pricing:  
    started = driver.find_element(By.XPATH, '/html/body/modularsignup-app/sequence/div[2]/bottom-bar/div/button/span[2]')
    started.click()
    temp = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[1]/div/div[3]/div[1]/div/span[2]/span'))
    )
    if find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[1]/div/div[3]/div[1]/div/span[2]/span', 1)[0]:
      df.at[index, '1_Gig'] = find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[1]/div/div[3]/div[1]/div/span[2]/span', 1)[1]
    if find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[2]/div/div[3]/div[1]/div/span[2]/span',1)[0]:
       df.at[index,'2_Gig'] = find_price(driver,'/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[2]/div/div[3]/div[1]/div/span[2]/span',1)[1]
    if find_price(driver,'/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[3]/div/div[3]/div[1]/div/span[2]/span',1)[0]:
       df.at[index, '5_Gig'] = find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[3]/div/div[3]/div[1]/div/span[2]/span',1)[1]
    if find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[4]/div/div[3]/div[1]/div/span[2]/span',1):
       df.at[index, '8_Gig'] = find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[4]/div/div[3]/div[1]/div/span[2]/span',1)[1]
  pricing = False


  df.to_csv(csvpath, index=False)
  
  driver.get("https://fiber.google.com/db/")


df.to_csv(csvpath, index=False)
driver.quit()


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")













# try:
  #   elements = WebDriverWait(driver, 1).until(
  #       EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mat-mdc-checkbox-2-input"]'))
  #   )
  #   df.at[index, 'status'] = 'Eligible'
  # except:
  #   try:
  #     elements1 = WebDriverWait(driver,1).until(
  #       EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/address-app/div/cta-view/cta-container/cta-mailing/div/div/div[1]/div/h1' ))
  #     )
  #     df.at[index,'status'] = 'Unavailable'
  #   except:
  #     try:
  #       element2 = WebDriverWait(driver,1).until(
  #         EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/address-app/div/cta-view/cta-container/cta-already-registered/div/h1'))
  #       )
  #       df.at[index,'status'] = 'Has Account'
  #     except:

  #       df.at[index, 'status'] = 'Need Apt'