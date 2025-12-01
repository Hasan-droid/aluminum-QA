from alumnium import Alumni
from selenium.webdriver import Chrome
import time

def test_login(al: Alumni, driver: Chrome):
    driver.get(f"http://10.0.81.222:5050/index-rtl.html")
    driver.maximize_window()
    time.sleep(3.5)

    al.do("Type 9951035944 into username field")
    al.do(("Type P@ssw0rd into password field"))
    al.do("click login button")
    time.sleep(5)