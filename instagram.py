# WORKING UPLOAD TO INSTA. JUST NEED TO CLICK UPLOAD
# ADD OPTION TO LOGIN AND CHECK IF COOKIES ARE REQUIRED
             
from selenium .webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pyautogui
import pickle
import time
from selenium import webdriver
COOKIES_BUTTON = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]"
USERNAME_XPATH = "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input"
PASSWORD_XPATH = "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[1]/div[2]/div/label/input"
LOGIN_BUTTON = "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]"
CREATE_CONTENT_SELECTOR = "[aria-label='New post']"
TURN_OFF_NOTIFICATIONS_XPATH = "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]"
UPLOAD_BUTTON = "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div/button"
CONFIRM_REELS_XPATH = "/html/body/div[2]/div/div/div[3]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div/div[4]/button"
UPLOAD_NEXT_XPATH = "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div[3]/div/div"
SELECT_THUMBNAIL_XPATH = "//*[contains(text(), 'Select From Computer')]"
UPLOAD_NEXT_2_XPATH = "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div[3]/div/div"
CAPTION_XPATH = "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div[1]"
FINAL_UPLOAD_XPATH = "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div[3]/div/div"

def load_cookie(driver: webdriver.Chrome, path):
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             driver.add_cookie(cookie)

def post_to_instagram(driver: webdriver.Chrome):
    driver.get("https://instagram.com")
    load_cookie(driver,'./insta_cookies.txt')
    print("loading cookies")
    driver.refresh()
    print('Turning off notifications')
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, TURN_OFF_NOTIFICATIONS_XPATH))
    )

    element.click()
    print('Clicking create content button')
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CREATE_CONTENT_SELECTOR))
    )
    element.click()
    print('Clicking upload video')
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, UPLOAD_BUTTON))
    )
    element.click()

    print('Waiting')
    time.sleep(2)
    print('Typing file path to video')
    pyautogui.typewrite(r"video filepath")
    pyautogui.press('enter')
    try:
        print('Confirming upload to reels')
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, CONFIRM_REELS_XPATH))
        )
        element.click()
    except NoSuchElementException:
        pass

    print("clicking next after selecting video")
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, UPLOAD_NEXT_XPATH))
    )

    element.click()


    print("Attempting to click on select thumbnail")
    time.sleep(1)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, SELECT_THUMBNAIL_XPATH))
    )
    element.click()

    time.sleep(2)
    pyautogui.typewrite(r"thumbnail filepath")
    pyautogui.press('enter')

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, UPLOAD_NEXT_2_XPATH))
    )
    element.click()

    element = driver.find_element(By.XPATH, CAPTION_XPATH)
    element.send_keys("This be a test caption")
    element = driver.find_element(By.XPATH, FINAL_UPLOAD_XPATH)
    element.click()
    input("continue?")