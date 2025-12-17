import pytest
from alumnium import Alumni
from selenium.webdriver import Chrome
import json
import time

@pytest.mark.scenario1
class TestServiceDefinition:
    # Class-level variables to share state between tests
    new_URL = None
    cooke_json = None

    @pytest.mark.order(1)
    def test_login(self, al: Alumni, driver: Chrome):
        driver.get(rf"http://172.16.2.56:3005/?redirect_uri=http%3A%2F%2F172.16.2.56%3A3002")
        driver.maximize_window()

        # al.do("Login with username = 'adminn' , password =  '123456789Aa@'")
        al.do("Type adminn into username field")
        al.do("Type 123456789Aa@ into password field")
        al.do("click sign in button")
        print("Done")
        time.sleep(6)

        # store URL for subsequent tests in this class
        TestServiceDefinition.new_URL = driver.current_url

    @pytest.mark.order(2)
    def test_create_GOS_service_subservice(self, al: Alumni, driver: Chrome):
        print(f"the new URL {TestServiceDefinition.new_URL}")
        driver.get(TestServiceDefinition.new_URL)

        al.do("hover the 'العربية' button on the navigation bar")
        al.do("Click the 'العربية' button on the navigation bar")

        al.do("Click on 'تعريف الخدمات' card")


        # Create a new GOS 
        al.do("Click on the 'إنشاء مجموعة جديدة' button")
        al.check("'إنشاء مجموعة جديدة' dialog is displayed")

        al.do("Type 'مجموعة للأتمتة' into 'اسم المجموعة باللغة العربية' field")
        al.do("Type 'GOS for automation' into 'اسم المجموعة باللغة الإنجليزية' field")
        
        al.do("select 'أفراد' option from 'نوع المجموعة' radio button group")
        al.do("Click on the 'حفظ' button")
        
        al.do("search for 'مجموعة للأتمتة' in the search box")
        al.check("'مجموعة للأتمتة' is displayed in the search results")

        # Create a new subservice
        al.do("Click on the 'الخدمات' sub-tab next to 'الخدمات الفرعية' sub-tab")

        al.do("hover on 'إنشاء خدمة جديدة' button")
        al.do("click on 'إنشاء خدمة جديدة' button")

        al.check("'إنشاء خدمة جديدة' dialog is displayed")

        al.do("Type 'خدمة للأتمتة' into 'اسم الخدمة باللغة العربية' field")
        al.do("Type 'Service for automation' into 'اسم الخدمة باللغة الإنجليزية' field")

        # select option from 'المجموعة' dropdown list using selenium
        
        # op1 = al.find("option 'مجموعة للأتمتة' inside the dropdown list last option")
        # op1.click()

        al.do("Click on the 'حفظ' button")

        driver.refresh()

        servicesArea = al.area("'تعريف الخدمات' box")
        servicesArea.do("click on the 'الخدمات' button next to 'مجموعة الخدمات' ")

        # al.do("Click on the 'الخدمات' sub-tab next to 'الخدمات الفرعية' sub-tab")
        # al.do("Click on the 'الخدمات' sub-tab next to 'مجموعات الخدمات' ")

        servicesArea.do("search for 'خدمة للأتمتة' in the search box")
        servicesArea.check("'خدمة للأتمتة' is displayed in the search results")


        # Create a new subservice

        subservicesArea = al.do("Click on the 'الخدمات الفرعية' button next to 'الخدمات' button")

        subservicesArea.do("click on 'إنشاء خدمة فرعية جديدة' button")
        al.check("'إنشاء خدمة فرعية جديدة' dialog is displayed")

        al.do("Type 'خدمة فرعية للأتمتة' into 'اسم الخدمة الفرعية باللغة العربية' field")
        al.do("Type 'Subservice for automation' into 'اسم الخدمة الفرعية باللغة الإنجليزية' field")
        al.do("type 'نص للأتمتة' into 'الوصف باللغة العربية' field")
        al.do("type 'Text for automation' into 'الوصف باللغة الإنجليزية' field")




        dr2 = al.find("'الخدمة' dropdown list")
        dr2.click()
        al.do("hover on 'خدمة للأتمتة' static text inside the dropdown list")
        al.do("click on 'خدمة للأتمتة' static text inside the dropdown list last option")
        # op2 = al.find("option 'خدمة للأتمتة' inside the dropdown list")
        # op2.click()

        # dr2 = al.find("'الخدمة' dropdown list")
        # dr2.click()
        # op2 = al.find("option 'خدمة للأتمتة' inside the dropdown list")
        # op2.click()

        # if al.check(" 'خدمة للأتمتة' is selected in the 'الخدمة' dropdown list"):
        #     pass
        # else:
        #     dr2 = al.find("'الخدمة' dropdown list")
        #     dr2.click()
        #     al.do("hover on 'خدمة للأتمتة' static text inside the dropdown list")
        #     op2 = al.find("option 'خدمة للأتمتة' inside the dropdown list")
        #     op2.click()

        al.do("Click on the 'حفظ' button")

        al.do("search for 'خدمة فرعية للأتمتة' in the search box")
        al.check("'خدمة فرعية للأتمتة' is displayed in the search results")

        cooke = driver.get_cookies()
        TestServiceDefinition.cooke_json = json.dumps(cooke)


    # @pytest.mark.order(3)
    # def test_after_login2(self, al: Alumni, driver: Chrome):
    #     cookies = json.loads(TestServiceDefinition.cooke_json) if TestServiceDefinition.cooke_json else []
    #     driver.get("http://172.16.2.56:3002/health")
    #     for cookie in cookies:
    #         driver.add_cookie(cookie)
    #     driver.get("http://172.16.2.56:3002/services/definition")

    #     al.do("Click on 'الخدمات الفرعية' sub-tab")