from test_setup import get_driver

def test_unknown_route_redirects_to_login():
    driver = get_driver()
    try:
        driver.get("http://65.0.27.191:3000/unknown-route")
        # check if login page elements exist
        assert "Login" in driver.page_source or driver.find_element("id", "login-btn")
    finally:
        driver.quit()
