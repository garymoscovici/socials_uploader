
import pickle
import time

import pyautogui
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def check_exists_by_xpath(driver ,xpath):
    try:
        
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def load_cookie(driver, path):
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             driver.add_cookie(cookie)

def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def post_to_tiktok(driver, test_mode, filename):
    LOGIN_TIKTOK_BUTTON_XPATH = "/html/body/div[7]/div[3]/div/div/div[1]/div[1]/div/div/a[2]/div/p"
    TIKTOK_ACCEPT_COOKIES = "/html/body/tiktok-cookie-banner//div/div[2]/button[2]"
    TIKTOK_UPLOAD_BUTTON = "/html/body/div[1]/div[1]/div/div[3]/div[1]/a/div/span"
    TIKTOK_SELECT_BUTTON = "/html/body/div[1]/div/div/div/div/div/div/div/div"
    TIKTOK_CAPTION_BOX = "/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div"
    LOADING_WHEEL = "/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/span/div/div[1]/div"
    POST_BUTTON = "/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div[8]/div[2]/button"
    "Use phone / email / username"


    driver.get("http://www.tiktok.com")
    try:
        load_cookie(driver,'./tiktok_cookies.txt')
    except:
        print("you need to login")
        input("Press Enter to continue...")
        save_cookie(driver, './tiktok_cookies.txt')
        load_cookie(driver,'./tiktok_cookies.txt')
        
    else:
        driver.refresh()
        
    print("Continuing")
    print("Clicking on upload")
    
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, TIKTOK_UPLOAD_BUTTON))
    )

    element.click()
    print("Clicking on select file")
    iframe = driver.find_element(By.CSS_SELECTOR, 'iframe')
    driver.switch_to.frame(iframe)
    time.sleep(3)
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, TIKTOK_SELECT_BUTTON))
    )
    ActionChains(driver).move_to_element(element).click(element).perform()
    time.sleep(2)
    pyautogui.typewrite(filename)
    pyautogui.press('enter')
    while True:
        time.sleep(1)
        try:
            element = driver.find_element(By.XPATH, LOADING_WHEEL)
            print("\r" + f"loading percent: {element.text}")
            # if int(re.findall(r'\d+',element.text)[0]) >=100:
            #     print("Finished uploading, continuing in 2 seconds...")
            #     time.sleep(2)
            #     raise NoSuchElementException
        except NoSuchElementException:
            print("Upload finished")
            time.sleep(1)
            break
        
    # input("Press enter once upload is complete")
    element = driver.find_element(By.XPATH, TIKTOK_CAPTION_BOX)
    element.click()
    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.DELETE)
    element.send_keys("This be a test caption")
    element = driver.find_element(By.XPATH, POST_BUTTON)
    if not test_mode:
        element.click()
    else:
        time.sleep(5)
    # driver.close()
    # input("close Driver?")
    return driver

