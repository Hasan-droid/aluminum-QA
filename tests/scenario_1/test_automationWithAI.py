import pytest
from alumnium import Alumni
from selenium.webdriver import Chrome
import json
import time

# Module-level variables to share state between tests
new_URL = None
cooke_json = None

@pytest.mark.scenario1
@pytest.mark.order(1)
def test_login(al: Alumni, driver: Chrome):
    driver.get(f"http://172.16.2.56:3005/?redirect_uri=http%3A%2F%2F172.16.2.56%3A3002")
    driver.maximize_window()
    time.sleep(3.5)
    
   # al.do("Login with username = 'adminn' , password =  '123456789Aa@'")
    al.do("Type adminn into username field")
    al.do("Type 123456789Aa@ into password field")
    al.do("click sign in button")
    print("Done")
    time.sleep(6)

    global new_URL
    new_URL = driver.current_url
    

@pytest.mark.scenario1
@pytest.mark.order(2)
def test_after_login(al: Alumni, driver: Chrome):
    global new_URL
    print(f"the new URL {new_URL}")
    driver.get(new_URL)
    
    
    al.do("hover the 'العربية' button on the navigation bar")
    al.do("Click the 'العربية' button on the navigation bar")

    al.do("Click on 'تعريف الخدمات' card")

    al.do("Click on 'الخدمات الفرعية' sub-tab")
    time.sleep(3)
    global cooke_json
    cooke = driver.get_cookies()
    cooke_json = json.dumps(cooke)
    time.sleep(3)
    
@pytest.mark.scenario1
@pytest.mark.order(3)
def test_after_login2(al: Alumni, driver: Chrome):
    global cooke_json
    cookies = json.loads(cooke_json) if cooke_json else []
    driver.get("http://172.16.2.56:3002/health")
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("http://172.16.2.56:3002/services/definition")
    
    al.do("Click on 'الخدمات الفرعية' sub-tab")