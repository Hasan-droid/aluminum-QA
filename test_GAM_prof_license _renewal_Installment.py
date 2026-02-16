# فحص تجديد رخصة مهنية ومحاكاة الدفع مع التأكد من إكمال الطلب

from alumnium import Alumni
from selenium.webdriver import Chrome
import time
from decimal import Decimal
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from Get_Captch import get_Captcha as captcha

payment_amount = None
payment_number = None
application_number = None

def test_license_renewal(al: Alumni, driver: Chrome):
    driver.get(fr"http://10.0.81.212:8080/index-rtl.html")
    driver.maximize_window()
    time.sleep(10)

    #تسجيل الدخول
    al.do("Type '9571018202' into 'اسم المستخدم / الرقم الوطني' field")
    al.do("Type 'P@ssw0rd' into password field")

    code = captcha()
    al.do(f"type {code} into the textbox (captcha) field above login button")

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
    al.do("type '3020' into 'رقم الرخصة' field")

    DDE = al.find("'المنطقة' dropdown field") # find dropdown element then click it
    DDE.click()
    option = al.find("option '1-المدينة' inside the dropdown list")
    option.click()

    al.check("'اكرم محمد سعيد لصوي' is in 'اسم المنشأة' field")
    print("التكامل بالخطوة الأولى تم")

    al.do("hover on 'التالي' button")
    al.do("click on 'التالي' button") 

    # الخطوة الثانية

    tableArea = al.area("'الغايات المسجلة على السجل التجاري' table") # التأكد من رقم الغاية
    tableArea.check("'620068' in 'رمز الغاية' column")
    print("تم التحقق من رمز الغاية في الخطوة الثانية")

    al.do("hover on 'التالي' button")
    al.do("click on 'التالي' button")


    # الخطوة الثالثة

    al.do("hover on 'موافق' button")
    al.do("click on 'موافق' button")

    al.do("hover the toggle button")
    al.do("click switch widget on 'الإقرار' box")
    print("تم التأكد من الإقرار في الخطوة الثالثة")

    al.do("hover on 'التالي' button")
    al.do("click on 'التالي' button")

    # الخطوة الرابعة
    al.check("'الرسوم' is in the step progress bar")
    print("تم التأكد من عرض الخطوة الرابعة")

    al.do("hover on 'تقسيط الرسوم' button")
    al.do("click on 'تقسيط الرسوم' button")

    al.do("hover on 'موافق' button")
    al.do("click on 'موافق' button")

    al.do("hover on 'موافق' button")
    al.do("click on 'موافق' button")

    global application_number
    application_number = al.get("application number from the popup window after 'رقم الطلب: '").strip()

    al.do("hover on 'موافق' button")
    al.do("click on 'موافق' button")
   


def test_login_to_FinanicalOfficer(al: Alumni, driver: Chrome):
    driver.get(f"http://10.35.21.51:9090/index-rtl.html")
    driver.maximize_window()
    time.sleep(10)
    # تسجيل الدخول
    al.do("type '57264' into 'اسم المستخدم / الرقم الوظيفي' field")
    al.do("Type '123456' into password field")

    # try:
    #     code = captcha()
    #     al.do(f"type {code} into the textbox (captcha) field above login button")
    # except Exception:
    #     pass

    al.do("click login button")
    print("تم تسجيل الدخول")

    # الطلبات

    inbox = al.area("صندوق الوارد box")
    inbox.do("hover on the number inside the 'الطلبات' card")
    inbox.do("click on the number inside the 'الطلبات' card")

    al.do("hover on 'بحث' button")
    al.do("click on 'بحث' button")

    global application_number
    al.do(f"type {application_number} into 'رقم الطلب' field")
    al.do("hover on 'بحث' button inside box")
    al.do("click on 'بحث' button inside box")   

    al.check(f"{application_number} number is displayed on the table")

    al.do(f"hover on {application_number} row")
    al.do(f"click on {application_number} row to make it selected")

    al.do("hover on 'عرض الطلب' button")
    al.do("click on 'عرض الطلب' button")

    al.do("hover on 'احتساب الاقساط' sub-tab(button)")
    al.do("click on 'احتساب الاقساط' sub-tab(button)")

    global payment_amount

    serviceFeesArea = al.area("'رسوم الخدمة' table")
    payment_amount = serviceFeesArea.get("the amount under 'القيمة' column")
    assert payment_amount is not None, "Payment amount not found"
    payment_amount = Decimal(str(payment_amount))
    payment_amount = payment_amount / 2

    paymentsArea = al.area("'الدفعات' box")

    #الدفعة الأولى
    paymentsArea.do("hover on 'جديد' button")
    paymentsArea.do("click on 'جديد' button")
    paymentsPopupArea = al.area("'الدفعات' popup")
    paymentsPopupArea.do("type '12' into 'رقم الدفعة' field")

    DDE3 = paymentsPopupArea.find("'نوع الدفعة' dropdown field")
    DDE3.click()
    option3 = paymentsPopupArea.find("option 'دفعة أولى' inside the dropdown list")
    option3.click()
    paymentsPopupArea.do("type '132' into 'رقم الشيك' field")
    paymentsPopupArea.do(f"type {payment_amount} into 'القيمة' field")

    tomorrow = (datetime.now(ZoneInfo("Asia/Amman")) + timedelta(days=1)).strftime(f"%Y/%m/%d")
    paymentsPopupArea.do(f"type {tomorrow} into 'تاريخ استحقاق الشيك' date field")

    paymentsPopupArea.do("hover on 'حفظ' button")
    paymentsPopupArea.do("click on 'حفظ' button")

    # القسط

    paymentsArea.do("hover on 'جديد' button")
    paymentsArea.do("click on 'جديد' button")
    paymentsPopupArea = al.area("'الدفعات' popup")
    paymentsPopupArea.do("type '123' into 'رقم الدفعة' field")

    DDE4 = paymentsPopupArea.find("'نوع الدفعة' dropdown field")
    DDE4.click()
    option4 = paymentsPopupArea.find("option 'قسط' inside the dropdown list")
    option4.click()
    paymentsPopupArea.do("type '132' into 'رقم الشيك' field")
    paymentsPopupArea.do(f"type {payment_amount} into 'القيمة' field")

    afterTomorrow = (datetime.now(ZoneInfo("Asia/Amman")) + timedelta(days=2)).strftime(f"%Y/%m/%d")
    paymentsPopupArea.do(f"type {afterTomorrow} into 'تاريخ استحقاق الشيك' date field")

    paymentsPopupArea.do("hover on 'حفظ' button")
    paymentsPopupArea.do("click on 'حفظ' button")

    al.do("hover on 'توزيع الدفعات' button")
    al.do("click on 'توزيع الدفعات' button")

    al.do("hover on 'موافق' button")
    al.do("click on 'موافق' button")

    al.do("hover on 'نعم' button")
    al.do("click on 'نعم' button")

    al.check("popup contains 'تم ارجاع الطلب الى مقدم الطلب' message")

    al.do("hover on 'موافق' button")
    al.do("click on 'موافق' button")


def test_create_payment_number(al: Alumni, driver: Chrome):
    driver.get(fr"http://10.0.81.212:8080/index-rtl.html")
    driver.maximize_window()
    time.sleep(10)

    #تسجيل الدخول
    al.do("Type '9571018202' into 'اسم المستخدم / الرقم الوطني' field")
    al.do("Type 'P@ssw0rd' into password field")

    code = captcha()
    al.do(f"type {code} into the textbox (captcha) field above login button")

    al.do("click login button")
    print("تم تسجيل الدخول")

    applicationsArea = al.area("'الطلبات' area that contains cards")
    applicationsArea.do("hover on 'بحاجة لإجراء' card(button)")
    applicationsArea.do("click on 'بحاجة لإجراء' card(button)")

    # بحث عن الطلب
    # al.do("hover on 'بحث' button")
    # al.do("click on 'بحث' button")

    # global application_number
    # al.do(f"type {application_number} into 'رقم الطلب' field")
    # al.do("hover on 'بحث' button inside box")
    # al.do("click on 'بحث' button inside box")   

    # al.check(f"{application_number} number is displayed on the table")

    # al.do(f"hover on {application_number} row")
    # al.do(f"click on {application_number} row to make it selected")

    # al.do("hover on 'عرض الطلب' button")
    # al.do("click on 'عرض الطلب' button")
    applicationMainInfoArea = al.area("'بيانات الطلب الرئيسية' section")
    applicationMainInfoArea.do("hover on 'احتساب الرسوم' button")
    applicationMainInfoArea.do("click on 'احتساب الرسوم' button")

    serviceFeesArea = al.area("'رسوم الخدمة' popup(form)")
    serviceFeesArea.do("hover on 'إنشاء رقم الدفع المرجعي' button")
    serviceFeesArea.do("click on 'إنشاء رقم الدفع المرجعي' button")

    global payment_number 

    serviceFeesArea2 = al.area("'أمانة عمّان الكبرى- رسوم الخدمة' popup(form)")
    payment_number = serviceFeesArea2.get("number from 'رقم الدفع المرجعى' field")

    serviceFeesArea2.do("hover on 'إغلاق' button")
    serviceFeesArea2.do("click on 'إغلاق' button")

    #مين الموظف اللي بعدين؟؟؟؟