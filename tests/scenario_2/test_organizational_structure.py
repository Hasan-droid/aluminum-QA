import pytest
from alumnium import Alumni
from selenium.webdriver import Chrome
import json
import time

@pytest.mark.scenario2
class TestOrganizationalStructure:
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
        
        time.sleep(6)

        # store URL for subsequent tests in this class
        TestOrganizationalStructure.new_URL = driver.current_url

    @pytest.mark.order(2)
    def test_create_Mu_De_Sec_Pos(self, al: Alumni, driver: Chrome):
        driver.get(TestOrganizationalStructure.new_URL)

        al.do("hover the 'العربية' button on the navigation bar")
        al.do("Click the 'العربية' button on the navigation bar")

        al.do("Hover over 'الهيكل التنظيمي' button on the navigation bar")
        al.do("Click on 'الهيكل التنظيمي' button on the navigation bar")

        onNavarea = al.area("'الهيكل التنظيمي' options list")
        onNavarea.do("Hover over 'تعريف الهيكل التنظيمي' button")
        onNavarea.do("Click on 'تعريف الهيكل التنظيمي' button")

        al.do("Hover on the search box")
        al.do("click on the search box")

        al.do("Hover on 'إضافة بلدية' button")
        al.do("Click on 'إضافة بلدية' button")


        fields = {
            'رمز البلدية' : 'AUT',
             'اسم البلدية بالعربية' : 'بلدية الأتمتة',
             'اسم البلدية بالإنجليزية' : 'Automation Municipality'
        }
        addMunArea = al.area("'إضافة بلدية' dialog")
        addMunArea.do(f"Fill the form with {fields}")
        al.do("Hover on 'حفظ' button")
        addMunArea.do("Click on 'حفظ' button")

        al.do("search for 'بلدية الأتمتة' in the search box")
        al.check("'بلدية الأتمتة' is displayed in the search results under 'اسم البلدية عربي' column")


        # Add a department ########################################################
        al.do("Hover over 'الإدارات' button")
        al.do("Click on 'الإدارات' button")

        al.do("Hover on 'إضافة إدارة' button")
        al.do("Click on 'إضافة إدارة' button")

        al.do("Type 'إدارة الأتمتة' into 'اسم الإدارة بالعربية' field")
        al.do("Type 'Automation Department' into 'اسم الإدارة بالإنجليزية' field")

        dr1 = al.find("'البلدية' dropdown list")
        dr1.click()
        dr_area = al.area("'البلدية' dropdown list")
        dr_area.do("click on 'بلدية الأتمتة - Automation Municipality' text")

        al.do("Hover on 'حفظ' button")
        al.do("Click on 'حفظ' button")

        driver.refresh()

        al.do("Hover over 'الإدارات' button")
        al.do("Click on 'الإدارات' button")

        al.do("Search for 'إدارة الأتمتة' in the search box")
        al.check("'إدارة الأتمتة' is displayed in the search results under 'اسم الإدارة عربي' column")

        # Add a section ########################################################
        al.do("Hover over 'الأقسام' button")
        al.do("Click on 'الأقسام' button")
        
        al.do("Hover on 'إضافة قسم' button")
        al.do("Click on 'إضافة قسم' button")
        
        al.do("Type 'قسم الأتمتة' into 'اسم القسم بالعربية' field")
        al.do("Type 'Automation Section' into 'اسم القسم بالإنجليزية' field")

        dr2 = al.find("'الإدارة' dropdown list")
        dr2.click()
        dr_area = al.area("'الإدارة' dropdown list")
        dr_area.do("click on 'إدارة الأتمتة - Automation Department' text")

        al.do("Hover on 'حفظ' button")
        al.do("Click on 'حفظ' button")

        driver.refresh()

        al.do("Hover over 'الأقسام' button")
        al.do("Click on 'الأقسام' button")
        
        al.do("Search for 'قسم الأتمتة' in the search box")
        al.check("'قسم الأتمتة' is displayed in the search results under 'اسم القسم عربي' column")

        # Add a position ########################################################
        al.do("Hover over 'المناصب' button")
        al.do("Click on 'المناصب' button")
        
        al.do("Hover on 'إضافة منصب' button")
        al.do("Click on 'إضافة منصب' button")
        
        al.do("Type 'منصب الأتمتة' into 'اسم المنصب بالعربية' field")
        al.do("Type 'Automation Position' into 'اسم المنصب بالإنجليزية' field")

        dr3 = al.find("'القسم' dropdown list")
        dr3.click()
        dr_area = al.area("'القسم' dropdown list")
        dr_area.do("click on 'قسم الأتمتة - Automation Section' text")

        al.do("Hover on 'حفظ' button")
        al.do("Click on 'حفظ' button")

        driver.refresh()

        al.do("Hover over 'المناصب' button")
        al.do("Click on 'المناصب' button")

        al.do("Search for 'منصب الأتمتة' in the search box")
        al.check("'منصب الأتمتة' is displayed in the search results under 'اسم المنصب عربي' column")    



        cooke = driver.get_cookies()
        TestOrganizationalStructure.cooke_json = json.dumps(cooke)


    @pytest.mark.order(3)
    def test_delete_Mu_De_Sec_Pos(self, al: Alumni, driver: Chrome):
        cookies = json.loads(TestOrganizationalStructure.cooke_json) if TestOrganizationalStructure.cooke_json else []
        driver.get("http://172.16.2.56:3002/health")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("http://172.16.2.56:3002/Organizational-structure/define")

        al.do("Search for 'بلدية الأتمتة' in the search box")
        al.check("'بلدية الأتمتة' is displayed in the search results under 'اسم البلدية عربي' column")

        mun_area = al.area("'بلدية الأتمتة' row")
        mun_area.do("click on the button in the first cell that contains image")

        dr_area= al.area("option dropdown list")
        dr_area.do("hover on 'حذف' button")
        dr_area.do("click on 'حذف' button")

        al.do("hover on 'حذف' button")
        al.do("click on 'حذف' button")