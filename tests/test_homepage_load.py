# selenium-tests/tests/test_homepage_load.py
from test_setup import get_driver

def test_homepage_title():
    driver = get_driver()
    try:
        driver.get("http://43.204.115.124:3000/")
        assert "Expense" in driver.title
    finally:
        driver.quit()
