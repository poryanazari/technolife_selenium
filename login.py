from selenium import webdriver
from selenium.common import *
from selenium import *
from selenium.webdriver import *
from selenium.webdriver.common.by import By
import time
import random
import string
import json
import requests
from persian_names import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def random_letters(length=8):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def setup_firefox_driver(allow_notifications=True):
    firefox_options = Options()
    
    if allow_notifications:
        # Allow notifications
        firefox_options.set_preference("dom.webnotifications.enabled", True)
        firefox_options.set_preference("permissions.default.desktop-notification", 1)
    else:
        # Block notifications
        firefox_options.set_preference("dom.webnotifications.enabled", False)
        firefox_options.set_preference("permissions.default.desktop-notification", 2)
    
    return webdriver.Firefox(options=firefox_options)


def generate_strong_password(length=12):
    """Generate a strong password with mixed characters"""
    chars = string.ascii_letters + string.digits
    while True:
        password = ''.join(random.choice(chars) for _ in range(length))
        # Ensure it contains at least one of each character type
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                ):
            return password


def generate_random_job():
    jobs = [
        "مهندس داده",
        "طراح گرافیک",
        "مدیر پروژه",
        "متخصص امنیت سایبری",
        "مهندس هوش مصنوعی",
        "مدیر پایگاه داده",
        "مدیر محصول",
        "تحلیلگر مالی",
        "متخصص کلود",
        "مهندس کنترل کیفیت"
    ]
    
    return random.choice(jobs)



env = {}
with open('env.json', 'r' , encoding="Utf-8") as file:
    env = json.load(file)


def save_env():
    with open('env.json', 'w', encoding='utf-8') as f:
        json.dump(env, f, ensure_ascii=False, indent=4)


def national_code_generator():
    number_list = []
    _sum = 0
    out = ""
    for i in reversed(range(2, 11)):
        _j = random.randint(0, 9)
        number_list.append(str(_j))
        _sum += _j * i
    _m = _sum % 11
    if _m < 2:
        number_list.append(str(_m))
    elif _m >= 2:
        number_list.append(str(11 - _m))
    return out.join(number_list)


def login_with_password():

    driver = setup_firefox_driver(True)

    driver.maximize_window()
    driver.get("https://www.technolife.com/account/Login?backTo=/")
    try:
        driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div[1]/form/label/input').send_keys(env["phone_number"])
        driver.find_element(By.XPATH ,'//*[@id="__next"]/div[3]/div[1]/form/div/button' ).click()
    except Exception as e :
        print("\r\n[!]can not insert phone Number")
        driver.quit()
        return False
    time.sleep(1)
    try:
        driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div[1]/form/label/input').send_keys(env["password"])
        driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div[1]/form/div/button[2]').click()
    except Exception as e:
        print("\r\n[!]can not insert password")
        driver.quit()

        return False
    
    time.sleep(3)

    if env["user_name"] in  driver.page_source:
        print("\r\n[*]login successs passs")
        driver.quit()
        return True
    else:
        print("\r\n[!]can not login")
        driver.quit()
        return False
    

def ifream_pass(driver):
    try:
        iframe = driver.find_element(By.ID, "webpush-onsite")
        driver.switch_to.frame(iframe)
        driver.find_element(By.ID , "allow").click()
        print("iframe is visible")
    except NoSuchElementException:
        pass

def complite_profile():

    driver = setup_firefox_driver(True)
    driver.maximize_window()
    driver.get("https://www.technolife.com/account/Login?backTo=/")
    try:
        driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div[1]/form/label/input').send_keys(env["phone_number"])
        driver.find_element(By.XPATH ,'//*[@id="__next"]/div[3]/div[1]/form/div/button' ).click()
    except Exception as e :
        print("\r\n[!]can not insert phone Number")
        driver.quit()
        return
    
    time.sleep(1)

    try:
        driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div[1]/form/label/input').send_keys(env["password"])
        driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div[1]/form/div/button[2]').click()
    except Exception as e:
        print("\r\n[!]can not insert password")
        driver.quit()
        return
    
    fullname = fullname_fa('r') 

    env["user_name"] = fullname
    env["last_name"] = fullname.split(" ")[-1]
    env["first_name"] = fullname.replace( fullname.split(" ")[-1] , "" )

    driver.get("https://www.technolife.com/profile/account-info")

    ifream_pass(driver)
    try:
        driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/main/div/div[2]/div[3]/div/div[2]/div[2]/div/div[1]/button').click()
        driver.find_element(By.XPATH , '//*[@id="1check"]').clear()
        driver.find_element(By.XPATH , '//*[@id="1check"]').send_keys(env["first_name"])
        driver.find_element(By.XPATH , '//*[@id="2check"]').clear()
        driver.find_element(By.XPATH , '//*[@id="2check"]').send_keys(env["last_name"])
        driver.find_element(By.XPATH , '//*[@id="portal-modal"]/div[1]/div/div/div/form/div/button').click()
    except Exception as e:
        print("\r\n[!]can not change name")
        driver.quit()
        return
    
    save_env()
    driver.get("https://www.technolife.com/profile/account-info")
    time.sleep(1)

    if env["last_name"] in driver.page_source:
        print("\r\n[*]change name successs passs")
    else:
        print("\r\n[!]can not change name")

    
    national_code = national_code_generator()
    env["national_code"] = national_code
    
    ifream_pass(driver)

    try:
        driver.find_element(By.XPATH , '/html/body/div[1]/div[3]/main/div/div[2]/div[3]/div/div[2]/div[2]/div/div[4]/button').click()
        
        #driver.execute_script("document.getElementsByName('national_code')[0].value = '"+ env["national_code"] +"' ")
        #driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH , '//*[@id="1check"]'))

        driver.find_element(By.XPATH , '/html/body/div[2]/div[4]/div/div/div/form/label[2]/input').clear()
        driver.find_element(By.XPATH , '/html/body/div[2]/div[4]/div/div/div/form/label[2]/input').send_keys(env["national_code"])

        driver.find_element(By.XPATH , '/html/body/div[2]/div[4]/div/div/div/form/div/button').click()
    except Exception as e:
        print("\r\n[!]can not change NATIONAL CODE")
        driver.quit()
        return
    
    save_env()
    driver.get("https://www.technolife.com/profile/account-info")
    time.sleep(1)

    if env["national_code"] in driver.page_source:
        print("\r\n[*]change NATIONAL CODE successs passs")
    else:
        print("\r\n[!]can not change NATIONAL CODE")


    env["user_email"] = random_letters() + "@gmail.com"

    ifream_pass(driver)

    try:
        driver.find_element(By.XPATH , '/html/body/div[1]/div[3]/main/div/div[2]/div[3]/div/div[2]/div[2]/div/div[2]/button').click()
        driver.find_element(By.XPATH , '/html/body/div[2]/div[2]/div/div/div/form/label/input').clear()
        driver.find_element(By.XPATH , '/html/body/div[2]/div[2]/div/div/div/form/label/input').send_keys(env["user_email"])
        driver.find_element(By.XPATH , '/html/body/div[2]/div[2]/div/div/div/form/div/button').click()
    except Exception as e:
        print("\r\n[!]can not change email")
        driver.quit()
        return
    
    
    save_env()
    driver.get("https://www.technolife.com/profile/account-info")
    time.sleep(1)

    if env["user_email"] in driver.page_source:
        print("\r\n[*]change email successs passs")
    else:
        print("\r\n[!]can not change email")

    
    env["user_job"] = generate_random_job()

    ifream_pass(driver)

    try:
        driver.find_element(By.XPATH , '/html/body/div[1]/div[3]/main/div/div[2]/div[3]/div/div[2]/div[2]/div/div[5]/button' ).click()
        driver.find_element(By.XPATH , '/html/body/div[2]/div[5]/div/div/div/form/label/input').clear()
        driver.find_element(By.XPATH , '/html/body/div[2]/div[5]/div/div/div/form/label/input').send_keys(env["user_job"])
        driver.find_element(By.XPATH , '/html/body/div[2]/div[5]/div/div/div/form/div/button').click()
    except Exception as e:
        print("\r\n[!]can not change job")
        driver.quit()
        return


    save_env()
    driver.get("https://www.technolife.com/profile/account-info")
    time.sleep(1)

    if env["user_job"] in driver.page_source:
        print("\r\n[*]change job successs passs")
    else:
        print("\r\n[!]can not change job")

    env["password"] = generate_strong_password(10)

    ifream_pass(driver)

    try:
        driver.find_element(By.XPATH , '/html/body/div[1]/div[3]/main/div/div[2]/div[3]/div/div[2]/div[2]/div/div[8]/button').click()
        driver.find_element(By.XPATH , '/html/body/div[2]/div[8]/div/div/div/form/label[2]/input').send_keys(env["password"])
        driver.find_element(By.XPATH , '/html/body/div[2]/div[8]/div/div/div/form/label[3]/input').send_keys(env["password"])
        driver.find_element(By.XPATH , '/html/body/div[2]/div[8]/div/div/div/form/div/button').click()
    except Exception as e:

        print("\r\n[!]can not change password")
        driver.quit()
        return
    
    save_env()

    login_with_password()


def send_error():
    pass


import requests

def login_reqs(phone):
    url = "https://api.sms.ir/v1/send/verify"

    payload = {
        "mobile": phone,  # Replace with recipient number
        "templateId": 966622,     # Replace with your template ID
        "parameters": [
            {
                "name": "MESSAGE",
                "value": "login"   # Replace with actual value
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
        'x-api-key': 'D3bFgYVcU9jgK0Of5LC2gdgvLp7zanjLM8r96Qq35h8USLgA7P0wTw6SPS2LZizc'  # Replace with your actual API key
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises exception for 4XX/5XX errors
        print(response.json())       # Print JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")




while True:
    if login_with_password() == False:
        
        login_reqs("09124847225")
        login_reqs("09916078746")
        login_reqs("09939922433")

    time.sleep(60*30)





# complite_profile()

    



#login_with_password()




