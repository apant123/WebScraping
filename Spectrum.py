from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
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
    
def wait_for_page_load(driver, timeout=100):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )



def scrape_address(df, index, address, zip):
    service = Service(executable_path="/Users/aravpant/Desktop/Projects/WebScraping/chromedriver")
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    pricing = False
    driver.get("https://www.spectrum.com/phx/address/localization?zip=%7Bzipcode%7D&a=%7Bencoded_address%7D")

    #result = {'address': address, 'zip': zip, 'status': 'pending', '1_Gig': '', '2_Gig': '', '5_Gig': '', '8_Gig': ''}
    
    try:
        elem = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mat-input-0"]'))
        )
        elem.clear()
        elem.send_keys(address)
        # spectrum = WebDriverWait(driver, 100).until(
        #     EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div[2]/div[2]/app-address-localization/app-bf-page-container/div/div/app-bf-template-engine/div/app-bf-address-localization/div/form/div/div[1]'))
        # )
        # spectrum.click()

        # addy = WebDriverWait(driver, 100).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="mat-input-1"]'))
        # )
        # addy.clear()
        # addy.click()
        # time.sleep(1)
        # if check_element(driver, '//*[@id="mat-option-236"]'):
        #   time.sleep(1)
        #   addy.send_keys("APT")
        

            


        zipcode = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mat-input-2"]'))
        )
        zipcode.clear()
        zipcode.send_keys(zip)
        zipcode.send_keys(Keys.RETURN)

        
        try:
            element = WebDriverWait(driver, 100).until(
                EC.any_of(
                    EC.url_contains("https://www.spectrum.com/phx/address/house-not-found"),
                    EC.url_contains("/phx/buy/products"),
                    EC.url_contains("https://www.spectrum.com/phx/address/out-of-footprint"),
                    EC.url_contains("https://www.spectrum.com/phx/address/existing-coverage"),
                    EC.url_contains("https://www.spectrum.com/phx/address/multiple-unit")
                )
            )
            current_url = driver.current_url
            if current_url == 'https://www.spectrum.com/phx/address/multiple-unit':
                actions = ActionChains(driver)
                actions.send_keys(Keys.ENTER).perform()
                Aptbox = driver.find_element_by_xpath('//*[@id="mat-input-3"]')
                value = Aptbox.get_attribute('value')
                print(value)
                Boxclick = WebDriverWait(driver, 100).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/div[2]/div[2]/app-address/app-bf-page-container/div/div/app-bf-template-engine/div/app-bf-address/div/div/div/span/div/div[3]/div/div/button'))
                )
                Boxclick.click()
                element = WebDriverWait(driver, 100).until(
                    EC.any_of(
                        EC.url_contains("https://www.spectrum.com/phx/address/house-not-found"),
                        EC.url_contains("/phx/buy/products"),
                        EC.url_contains("https://www.spectrum.com/phx/address/out-of-footprint"),
                        EC.url_contains("https://www.spectrum.com/phx/address/existing-coverage"),
                        EC.url_contains("https://www.spectrum.com/phx/address/multiple-unit")
                    )
                )
        except TimeoutException:
            df.at[index, 'Spectrum-Status'] = 'Something'
        
        current_url = driver.current_url

        # if current_url == 'https://www.spectrum.com/phx/address/multiple-unit':
        #     actions = ActionChains(driver)
        #     actions.send_keys(Keys.ENTER).perform()
        #     Aptbox = driver.find_element_by_xpath('//*[@id="mat-input-3"]')
        #     value = Aptbox.get_attribute('value')
        #     print(value)
        #     Boxclick = WebDriverWait(driver, 100).until(
        #         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/div[2]/div[2]/app-address/app-bf-page-container/div/div/app-bf-template-engine/div/app-bf-address/div/div/div/span/div/div[3]/div/div/button'))
        #     )
        #     Boxclick.click()



        if "/phx/buy/products" in current_url:
            df.at[index, 'Spectrum-Status'] = 'Eligible'
            #pricing = True
            print("Eligible")
            
        elif current_url == 'https://www.spectrum.com/phx/address/out-of-footprint':
            df.at[index, 'Spectrum-Status'] = 'Unavailable'
            print("Unavailable")
        elif current_url == 'https://www.spectrum.com/phx/address/existing-coverage':
            df.at[index, 'Spectrum-Status'] = 'Has Account'
            print("Has Account")
        elif current_url == "https://www.spectrum.com/phx/address/multiple-unit":
            df.at[index, 'Spectrum-Status'] = 'Need Apt'

            print("Need Apt")
        elif current_url == 'https://www.spectrum.com/phx/address/house-not-found':
            df.at[index, 'Spectrum-Status'] = 'Call In'
            print("Call In")
        else:
            df.at[index, 'Spectrum-Status'] = 'Something'

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
            if find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[4]/div/div[3]/div[1]/div/span[2]/span',1)[0]:
                df.at[index, '8_Gig'] = find_price(driver, '/html/body/modularsignup-app/sequence/div[1]/main/div[2]/div/internet-step/section/div[3]/div[2]/broadband-label-list/div/div/broadband-label[4]/div/div[3]/div[1]/div/span[2]/span',1)[1]
    except Exception as e:
        print(f"Error processing address {address}: {e}")
    finally:
        driver.quit()
    




def main():
    total_time = 0
    num_runs = 1
    
    for i in range(num_runs):
        start_time = time.time()

        df = pd.read_csv('/Users/aravpant/Desktop/Projects/WebScraping/AddressList/small.csv')
        csvpath = '/Users/aravpant/Desktop/Projects/WebScraping/AddressList/ad5.csv'

        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = [executor.submit(scrape_address, df, index, row['address_primary'], row['zip']) for index, row in df.iterrows()]
            for future in as_completed(futures):
                future.result()  # Ensure all threads complete

       

            




        df.to_csv(csvpath, index=False)

        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time
        print(f"Run {i+1}: {elapsed_time:.2f} seconds")

    average_time = total_time / num_runs
    print(f"Average time over {num_runs} runs: {average_time:.2f} seconds")

if __name__ == "__main__":
    #cProfile.run('main()')
    main()
# Appedning to existing database







# //*[@id="mat-option-224"]

#//*[@id="mat-option-236"]

# //*[@id="mat-option-236"]


# "mat-mdc-autocomplete-panel mdc-menu-surface mdc-menu-surface--open ng-trigger ng-trigger-panelAnimation ng-tns-c1630904807-45 mat-mdc-autocomplete-visible mat-primary ng-star-inserted"