from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import cProfile


from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import time


def check_element(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
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

def check_element(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        return True
    except:
        return False

def find_price(driver, xpath, timeout):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return [True, element.text]
    except:
        return [False, "Null"]

def scrape_address(driver, address, zip):
    pricing = False
    result = {'address': address, 'zip': zip, 'status': 'pending', '1_Gig': '', '2_Gig': '', '5_Gig': '', '8_Gig': ''}
    
    try:
        driver.get("https://fiber.google.com/db/")

        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.address-checker__input.address-checker__input--street.borderable.pac-target-input"))
        )
        elem.clear()
        elem.send_keys(address)

        zipcode = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="hero-carousal"]/div[2]/div/div[1]/form/div/div[1]/div[3]/input'))
        )
        zipcode.clear()
        zipcode.send_keys(zip)
        zipcode.send_keys(Keys.RETURN)


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
            result['status'] = 'Something'








        if check_element(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div/div/base-step/section/preconfig-step/div/preconfig-card/div'):
            result['status'] = 'Eligible'
            pricing = True
        elif check_element(driver, '/html/body/div[1]/address-app/div/cta-view/cta-container/cta-mailing/div/div/div[1]/div/h1'):
            result['status'] = 'Unavailable'
        elif check_element(driver, '/html/body/div[1]/address-app/div/cta-view/cta-container/cta-already-registered/div/h1'):
            result['status'] = 'Has Account'
        elif check_element(driver, '/html/body/div[1]/address-app/div/cta-view/address-search/button/span[2]'):
            result['status'] = 'Need Apt'
        elif check_element(driver, '//*[@id="mat-radio-2-input"]'):
            result['status'] = 'Business'
        else:
            result['status'] = 'Something'

        if pricing:
            started = driver.find_element(By.XPATH, '/html/body/modularsignup-app/sequence/div[2]/bottom-bar/div/button/span[2]')
            started.click()
            temp = WebDriverWait(driver, 10).until(
              EC.presence_of_element_located((By.XPATH, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[1]/div/div[3]/div[1]/div/span[2]/span'))
            )
            if find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[1]/div/div[3]/div[1]/div/span[2]/span', 1)[0]:
                result['1_Gig'] = find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[1]/div/div[3]/div[1]/div/span[2]/span', 1)[1]
            if find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[2]/div/div[3]/div[1]/div/span[2]/span', 1)[0]:
                result['2_Gig'] = find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[2]/div/div[3]/div[1]/div/span[2]/span', 1)[1]
            if find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[3]/div/div[3]/div[1]/div/span[2]/span', 1)[0]:
                result['5_Gig'] = find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[3]/div/div[3]/div[1]/div/span[2]/span', 1)[1]
            if find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[4]/div/div[3]/div[1]/div/span[2]/span', 1)[0]:
                result['8_Gig'] = find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[4]/div/div[3]/div[1]/div/span[2]/span', 1)[1]
    except Exception as e:
        print(f"Error processing address {address}: {e}")
    
    return result

def create_driver():
    service = Service(executable_path="/Users/aravpant/Desktop/Projects/WebScraping/First-Project/chromedriver")
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver

def main():
    total_time = 0
    num_runs = 1
    
    for i in range(num_runs):
        start_time = time.time()

        df = pd.read_csv('/Users/aravpant/Desktop/Projects/WebScraping/AddressList/small.csv')
        csvpath = '/Users/aravpant/Desktop/Projects/WebScraping/AddressList/ad3.csv'

        results = []

        # Create a pool of WebDriver instances (equal to the number of threads)
        drivers = [create_driver() for _ in range(4)]

        try:
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(scrape_address, drivers[index % 4], row['address_primary'], row['zip']) for index, row in df.iterrows()]
                for future in as_completed(futures):
                    results.append(future.result())

            # Convert results to DataFrame and save to CSV
            results_df = pd.DataFrame(results)
            results_df.to_csv(csvpath, index=False)
        
        finally:
            # Close all WebDriver instances
            for driver in drivers:
                driver.quit()

        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time
        print(f"Run {i+1}: {elapsed_time:.2f} seconds")

    average_time = total_time / num_runs
    print(f"Average time over {num_runs} runs: {average_time:.2f} seconds")

if __name__ == "__main__":
    main()



#Done in an effort to not close the chrome tab out.