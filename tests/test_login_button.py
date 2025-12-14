# selenium-tests/tests/test_login_button.py
from test_setup import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_button_exists():
    driver = get_driver()
    try:
        driver.get("http://52.66.246.182:3000/")
        wait = WebDriverWait(driver, 6)
        button = wait.until(EC.presence_of_element_located((By.ID, "login-btn")))
        assert button.is_displayed()
    finally:
        driver.quit()
