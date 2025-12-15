# selenium-tests/tests/test_login_invalid.py
from test_setup import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_invalid_login():
    driver = get_driver()
    try:
        driver.get("http://43.204.115.124:3000/login")
        wait = WebDriverWait(driver, 6)
        wait.until(EC.presence_of_element_located((By.ID, "email")))

        driver.find_element(By.ID, "email").send_keys("wrong@example.com")
        driver.find_element(By.ID, "password").send_keys("wrongpassword")
        driver.find_element(By.ID, "login-btn").click()

        # after invalid login we expect to remain on /login (or show #login-error)
        wait.until(EC.presence_of_element_located((By.ID, "login-error")))
        assert "/login" in driver.current_url or "error" in driver.page_source.lower()
    finally:
        driver.quit()
