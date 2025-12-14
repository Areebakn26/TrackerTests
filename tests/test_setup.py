# selenium-tests/tests/test_setup.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import time

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    # disable GPU for CI
    options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(2)  # short implicit wait
    return driver

def login(driver, email=None, password=None):
    """
    Navigate to /login and perform sign in. credentials from env:
    TEST_EMAIL, TEST_PASSWORD. Defaults: test@example.com / 123456
    """
    email = email or os.environ.get("TEST_EMAIL", "aimen@gmail.com")
    password = password or os.environ.get("TEST_PASSWORD", "123456")

    driver.get("http://52.66.246.182:3000")

    wait = WebDriverWait(driver, 10)
    # wait for email field
    wait.until(EC.presence_of_element_located((By.ID, "email")))

    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(email)

    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)

    driver.find_element(By.ID, "login-btn").click()

    # wait until dashboard loads (either by URL or by seeing the Add Expense button)
    try:
        wait.until(EC.url_contains("/dashboard"))
    except:
        # fallback: wait for save button
        wait.until(EC.presence_of_element_located((By.ID, "save-btn")))

    # small pause to let React mount fully
    time.sleep(0.5)
