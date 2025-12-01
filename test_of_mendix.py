from alumnium import Alumni
from langchain_core.runnables.config import P
from selenium.webdriver import Chrome
import time

def test_login(al: Alumni, driver: Chrome):
    driver.get(f"https://193.188.64.53/index-rtl.html")
    driver.maximize_window()
    time.sleep(7)

    al.do("Type 9951035944 into 'اسم المستخدم / الرقم الوطني' field")
    print("username done")
    al.do(("Type P@ssw0rd into password field"))
    print("password done")
    time.sleep(5)
    al.do("click login button")
    print("login button done")
    time.sleep(5)
    al.do("click 'موافق' button")
    print("موافق button done")
    time.sleep(3)


