from alumnium import Alumni
from selenium.webdriver import Chrome
import time

# Module-level variable to share URL between tests
new_URL = None

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
    

def test_after_login(al: Alumni, driver: Chrome):
    global new_URL
    print(f"the new URL {new_URL}")
    driver.get(new_URL)
    

    al.do("hover the 'العربية' button on the navigation bar")
    al.do("Click the 'العربية' button on the navigation bar")
    