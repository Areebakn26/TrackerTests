# selenium-tests/tests/test_navigation_links.py
from test_setup import get_driver, login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_navigation():
    driver = get_driver()
    try:
        login(driver)   # <-- LOGIN REQUIRED BEFORE DASHBOARD
        
        wait = WebDriverWait(driver, 10)

        # Now homepage/dashboard will load correctly
        driver.get("http://43.204.115.124:3000/")

        topbar = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "top-bar"))
        )
        assert topbar.is_displayed()
    finally:
        driver.quit()
