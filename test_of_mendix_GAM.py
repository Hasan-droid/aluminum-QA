from alumnium import Alumni
from selenium.webdriver import Chrome
import time
from pathlib import Path


application_number = None

def test_login(al: Alumni, driver: Chrome):
    driver.get(f"http://10.35.21.51:9090/index-rtl.html")
    driver.maximize_window()

    al.do("Type '5538' into 'اسم المستخدم / الرقم الوظيفي' field")
    print("username done")
    al.do(("Type 19700434Aa@ into password field"))
    print("password done")
    al.do("click login button")
    print("login button done")
    
    al.do("hover the 'رخص المهن' button")
    al.do("click the 'رخص المهن' button")
    print("رخص المهن button done")
    

    al.do("hover the 'تجديد رخصة مهن' button")
    al.do("Click 'تجديد رخصة مهن' where color = #17347B ")
    print("blue arrow done")
    
    al.do("hover the 'التالي' button")
    al.do("click 'التالي' button")
    print("التالي button done")

    # Step 1
    al.do("type '9651000530' into 'الرقم الوطني / الشخصي' field")
    print("الرقم الوطني / الشخصي field done")
    al.do("type 'QMI97138' into 'رقم الهوية' field")
    print("رقم الهوية field done")
    al.do("insert '782490023' into 'رقم الهاتف' field")
    print("رقم الهاتف field done")
    al.do("type '11440' into 'رقم الرخصة' field")
    print("رقم الرخصة field done")
    time.sleep(3)
    al.do("click on 'الرقم الوطني للمنشأة' field")
    al.check("'الرقم الوطني للمنشأة' field contains '200060788' ")
    print("الرقم الوطني للمنشأة field checked")
    al.do("hover the 'التالي' button")
    al.do("click 'التالي' button")
    print("التالي button done")

    # Step 2
    area = al.area("'الغايات المسجلة على السجل التجاري' table")
    al.check("'الغايات المسجلة على السجل التجاري' table contains '832565'")
    print("الغايات المسجلة على السجل التجاري table checked")
    al.do("hover the 'التالي' button")
    al.do("click 'التالي' button")
    print("التالي button done")

    # Step 3
    al.do("hover the toggle button")
    al.do("click switch widget on 'الإقرار' box")
    print("الإقرار toggle button done")
    al.do("hover the 'التالي' button")
    al.do("click 'التالي' button")
    print("التالي button done")
    al.do("hover the 'موافق' button")
    al.do("click on 'موافق' button")
    print("موافق button done")

    # Step 4
    al.do("hover the 'تقديم الطلب' button")
    al.do("click on 'تقديم الطلب' button")
    print("تقديم الطلب button done")
    al.do("hover the 'موافق' button")
    al.do("click on 'موافق' button")
    print("موافق button done")

    global application_number
    application_number = al.get("application number")
    print(f"application number: {application_number}")

def test_login_to_Admin(al: Alumni, driver: Chrome):
    driver.get(f"http://10.35.21.52:9090/index-rtl.html")
    driver.maximize_window()

    al.do("type 'sec' into 'اسم المستخدم / الرقم الوظيفي' field")
    print("username done")
    al.do(("Type 19700434Aa@ into password field"))
    print("password done")
    al.do("click login button")
    print("login button done")

    DDE = al.find("'Development' dropdown link on the navigation bar")
    DDE.click()
    option = al.find("option 'استعلام عن طلبات' inside the dropdown list")
    option.click()

    al.do("hover on 'بحث' then click on it")

    global application_number

    al.do(f"type '{application_number}' into 'رقم الطلب' field")
    print("application number done")
    al.do("hover on 'بحث' inside the box")
    al.do("click on 'بحث' button inside the box")

    al.do("hover on 'إلغاء الطلب' button")
    al.do("click on 'إلغاء الطلب' button")
    print("إلغاء الطلب button done")

    al.do("hover on 'موافق' button")
    al.do("click on 'موافق' button")
    print("موافق button done")





def test_login_and_upload(al: Alumni, driver: Chrome):
    driver.get(f"http://10.35.21.51:9090/index-rtl.html")
    driver.maximize_window()

    al.do("Type '5538' into 'اسم المستخدم / الرقم الوظيفي' field")
    print("username done")
    al.do(("Type 19700434Aa@ into password field"))
    print("password done")
    al.do("click login button")
    print("login button done")
    
    al.do("hover the 'دائرة الأملاك  button")
    al.do("click the 'دائرة الأملاك ' button")
    print(" دائرة الأملاك button done")
    

    al.do("hover the 'تاجير املاك الامانة' button")
    al.do("Click 'تاجير املاك الامانة' button ")
    print(" تاجير املاك الامانة button done")

    # Step 1
    al.do("type '9651000530' into 'الرقم الوطني' field")
    print("الرقم الوطني field done")
    al.do("type 'QMI97138' into 'رقم الهوية' field")
    print("رقم الهوية field done")
    al.do("insert '00962782490023' into 'رقم الهاتف' field on the first section")
    print("رقم الهاتف field done")

    dr1 = al.find("'نوع مقدم الطلب' dropdown list")
    dr1.click()
    op1 = al.find("option 'المستأجر نفسه' inside the dropdown list")
    op1.click()

    al.do("hover on 'التالي' button")

    dr2 = al.find("'نوع العقار' dropdown list")
    dr2.click()
    op2 = al.find("option 'الأراضي' inside the dropdown list")
    op2.click()

    al.do("type 'عشوائي' into 'وصف الموقع' field ")
    al.do("hover on 'التالي' button")

    al.do("type 'عشوائي' into 'اسم الشارع' field ")
    al.do("type 'عشوائي' into 'صفة الإستعمال' field ")

    al.do("hover on 'التالي' button")
    al.do("click on 'التالي' button")

    # Step 2

    al.do("hover on 'اضافة مرفق جديد ' button")
    al.do("click on 'اضافة مرفق جديد ' button")

    al.do("type 'عشوائي' into 'إسم المرفق' field")

    file_path = Path(r"/root/aluminum-QA/Screenshot2025-02-09093907.png")
    file_input = al.find("file upload input next to 'تحميل' in the 'إضافة - تعديل مرفق' dialog")
    file_input.send_keys(str(file_path))

    # al.do("upload 'Screenshot2025-02-09093907.png' file into 'تحميل' field ")

    al.do("hover on 'حفظ' button ")
    al.do("click on 'حفظ' button ")

    # al.check("'المرفقات' table contains 'عشوائي' on 'إسم المرفق' column")

  
    # al.do("hover the toggle button")
    # al.do("click switch widget on 'الإقرار' box")
    # print("الإقرار toggle button done")