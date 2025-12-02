from alumnium import Alumni
from langchain_core.runnables.config import P
from selenium.webdriver import Chrome
import time

from sqlalchemy.orm import contains_alias

def test_login(al: Alumni, driver: Chrome):
    driver.get(f"https://193.188.64.53/index-rtl.html")
    driver.maximize_window()
    time.sleep(7)

    al.do("Type 9951035944 into 'اسم المستخدم / الرقم الوطني' field")
    print("username done")
    al.do(("Type P@ssw0rd into password field"))
    print("password done")
    time.sleep(2)
    # code = al.get("text from PNG image under password field, captcha div", vision=True)
    # print(f"captcha done{code}")
    # time.sleep(2)
    # al.do(f"Type {code} into field under the PNG image")
    # print("captcha field done")
    # time.sleep(2)
    al.do("click login button")
    print("login button done")
    time.sleep(5)
    al.do("click 'موافق' button")
    print("موافق button done")
    time.sleep(2)
    al.do("Click 'طلباتي' button")
    print("طلباتي button done")
    time.sleep(2)
    al.do("click 'x' button on the popup")
    print("x button done")

    area = al.area("03/12/2025 box")
    app_number = area.get("Application number")
    assert app_number is not None, "Application number field is missing"
    app_number_str = str(app_number)
    assert "2500520121" in app_number_str, f"Application number is not correct: {app_number_str}"