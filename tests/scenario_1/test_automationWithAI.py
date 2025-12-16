import pytest
from alumnium import Alumni
from selenium.webdriver import Chrome
import json
import time

@pytest.mark.scenario1
class TestAutomationWithAI:
    # Class-level variables to share state between tests
    new_URL = None
    cooke_json = None

    @pytest.mark.order(1)
    def test_login(self, al: Alumni, driver: Chrome):
        driver.get(rf"http://172.16.2.56:3005/?redirect_uri=http%3A%2F%2F172.16.2.56%3A3002")
        driver.maximize_window()
        time.sleep(3.5)

        # al.do("Login with username = 'adminn' , password =  '123456789Aa@'")
        al.do("Type adminn into username field")
        al.do("Type 123456789Aa@ into password field")
        al.do("click sign in button")
        print("Done")
        time.sleep(6)

        # store URL for subsequent tests in this class
        TestAutomationWithAI.new_URL = driver.current_url

    @pytest.mark.order(2)
    def test_after_login(self, al: Alumni, driver: Chrome):
        print(f"the new URL {TestAutomationWithAI.new_URL}")
        driver.get(TestAutomationWithAI.new_URL)

        al.do("hover the 'العربية' button on the navigation bar")
        al.do("Click the 'العربية' button on the navigation bar")

        al.do("Click on 'تعريف الخدمات' card")

        al.do("Click on 'الخدمات الفرعية' sub-tab")
        time.sleep(3)

        cooke = driver.get_cookies()
        TestAutomationWithAI.cooke_json = json.dumps(cooke)
        time.sleep(3)

    @pytest.mark.order(3)
    def test_after_login2(self, al: Alumni, driver: Chrome):
        cookies = json.loads(TestAutomationWithAI.cooke_json) if TestAutomationWithAI.cooke_json else []
        driver.get("http://172.16.2.56:3002/health")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("http://172.16.2.56:3002/services/definition")

        al.do("Click on 'الخدمات الفرعية' sub-tab")