from alumnium import Alumni
from selenium.webdriver import Chrome
import time

def test_login(al: Alumni, driver: Chrome):
    print(f"Current URL before navigation: {driver.current_url}")
    driver.get(f"http://172.16.2.56:3005/?redirect_uri=http%3A%2F%2F172.16.2.56%3A3002")
    print(f"Current URL after navigation: {driver.current_url}")
    driver.maximize_window()
    time.sleep(2)  # Wait 2 seconds to see the page load
    
    # Verify we're on the right page
    assert "172.16.2.56:3005" in driver.current_url, f"Expected to be on login page, but was on {driver.current_url}"
    
    print("Changing language")
    

    print("Changing language")
 

    # al.do("Click  on the arabic language button 'العربية' on the navigation bar")

    print("fill in fields 1")
   # al.do("Login with username = 'adminn' , password =  'admin'")
    al.do("Type adminn into username field")

    print("fill in fields 2")
    al.do("Type 123456789Aa@ into password field")

    al.do("click sign in button")
    print("Done")

    al.do("hover the 'العربية' button on the navigation bar")

    al.do("Click the 'العربية' button on the navigation bar")

    # time.sleep(1)
    # al.do("Enter ID number 'adminn' in the ID number field above password field")
    time.sleep(1)  # Wait 3 seconds to see the login result
    
    # Check if logged in (you may need to adjust this based on what indicates successful login)
    # logged_in = al.check("User is logged in successfully")
    # assert logged_in, "Login failed"
    # Keep browser open for 5 more seconds before closing