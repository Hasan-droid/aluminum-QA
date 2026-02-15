from alumnium import Alumni
from selenium.webdriver import Chrome
import time
from Get_Captch import get_Captcha as captcha

payment_number = None

def test_license_renewal(al: Alumni, driver: Chrome):
    driver.get(fr"http://10.0.81.212:8080/index-rtl.html")
    driver.maximize_window()
    time.sleep(10)

    #تسجيل الدخول
    al.do("Type '9721041581' into 'اسم المستخدم / الرقم الوطني' field")
    al.do(("Type '19700434Aa@' into password field"))
    code = captcha()
    al.do(f"type {code} into the textbox (captch) above login button")
    al.do("click login button")
    print("تم تسجيل الدخول")


    # بدء الخدمة 
    al.do("hover the 'تجديد رخصة مهن' button")
    al.do("click on the 'تجديد رخصة مهن' button")
    al.check("'الإرشادات العامة' text is displayed on the page")

    al.do("Hover on 'التالي' button")
    al.do("click on the 'التالي' button")
    al.check("'خدمة تجديد رخصة مهنية' text is displayed on the page")
    print("تم بدء الخدمة")


    # إدخال البيانات

    # الخطوة الأولى
    al.do("type '3519' into 'رقم الرخصة' field")

    DDE = al.find("'المنطقة' dropdown link on the navigation bar") # find dropdown element then click it
    DDE.click()
    option = al.find("option 'المدينة' inside the dropdown list")
    option.click()

    al.check("'احمد اسعد احمد خيرالله' is in 'اسم المنشأة' field")
    print("التكامل بالخطوة الأولى تم")

    al.do("hover on 'التالي' button")
    al.do("click on 'التالي' button") 

    # الخطوة الثانية

    tableArea = al.area("'الغايات المسجلة على السجل التجاري' table") # التأكد من رقم الغاية
    tableArea.check("'620005' in 'رمز الغاية' column")
    print("تم التحقق من رمز الغاية في الخطوة الثانية")

    al.do("hover on 'التالي' button")
    al.do("click on 'التالي' button")


    # الخطوة الثالثة
    al.do("hover the toggle button")
    al.do("click switch widget on 'الإقرار' box")
    print("تم التأكد من الإقرار في الخطوة الثالثة")

    al.do("hover on 'التالي' button")
    al.do("click on 'التالي' button")

    # الخطوة الرابعة
    al.check("'الرسوم' is in the step progress bar")
    print("تم التأكد من عرض الخطوة الرابعة")

    al.do("hover on 'تقديم الطلب' button")
    al.do("click on 'تقديم الطلب' button")
    al.do("hover on 'موافق' button")
    al.do("click on 'موافق' button")

    global payment_number
    payment_number = al.get("'رقم الدفع المرجع'payment number")
    print(f"application number: {payment_number}")
    print("تم تقديم الطلب في الخطوة الرابعة")

    al.do("hover on 'إغلاق' button")
    al.do("click on 'إغلاق' button")


def test_login_to_Admin(al: Alumni, driver: Chrome):
    driver.get(f"http://10.35.21.51:9090/index-rtl.html")
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

    global payment_number

    al.do(f"type '{payment_number}' into 'رقم الطلب' field")
    print("application number done")
    al.do("hover on 'بحث' inside the box")
    al.do("click on 'بحث' button inside the box")

    al.do("hover on 'إلغاء الطلب' button")
    al.do("click on 'إلغاء الطلب' button")
    print("إلغاء الطلب button done")

    al.do("hover on 'موافق' button")
    al.do("click on 'موافق' button")
    print("موافق button done")
