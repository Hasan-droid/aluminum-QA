from alumnium import Alumni
from selenium.webdriver import Chrome
import time
import pandas as pd

global df
global Data
global DataRows
global subServiceType

subServiceType = "خدمة تعديل تنظيمي"

df = pd.read_excel(r"Dummt.xlsx")
Data = df.to_dict('records')
DataRows = len(Data)

def test_login(al: Alumni, driver: Chrome):
    driver.get(f"http://10.35.24.158:5051/index-rtl.html")
    driver.maximize_window()
    time.sleep(12)
    # تسجيل الدخول
    al.do("type MxAdmin into 'اسم المستخدم / الرقم الوظيفي' field")
    al.do("Type P@ssw0rd into password field")
    al.do("click login button")
    print("تم تسجيل الدخول")

    global df
    global Data
    global DataRows
    global subServiceType



    DDE = al.find("'Development' dropdown link on the navigation bar")
    DDE.click()
    option = al.find("option 'تسلسل إجراء خدمات التنظيم والأملاك' inside the dropdown list")
    option.click()

    al.do("hover on 'بحث' button")
    al.do("click on 'بحث' button")

    al.do(f"type '{subServiceType}' into 'نوع الخدمة الفرعي' field")
    al.do("hover on 'بحث' inside the box")
    al.do("click on 'بحث' button inside the box") 

    al.do("hover on 'تسلسل الإجراء الجديد' button (sub-tab)")
    al.do("click on 'تسلسل الإجراء الجديد' button (sub-tab)") 

    for i in range(DataRows):
        ActionTypeCode= Data[i]['ActionTypeCode']
        FromStatusCode= Data[i]['FromStatusCode']
        FromRole= Data[i]['FromRole']
        ToStatusCode= Data[i]['ToStatusCode']
        ToRole= Data[i]['ToRole']
        MainStatusCode= Data[i]['MainStatusCode']
        InboxStatus= Data[i]['InboxStatus']  

        try: 
            al.do("hover on 'جديد' button")
            al.do("click on 'جديد' button")

            PopupArea = al.area("'إضافة - تعديل تسلسل الإجراء' popup")

            PopupArea.do("hover on the button of 'نوع الإجراء' field ")
            PopupArea.do("click on the button of 'نوع الإجراء' field ")
            PopupArea.do("hover on 'بحث' button")
            PopupArea.do("click on 'بحث' button")
            PopupArea.do(f"type {ActionTypeCode} into 'الرمز' field")
            PopupArea.do("hover on 'بحث' button inside the box")
            PopupArea.do("click on 'بحث' button inside the box")
            PopupArea.do("hover on the first row of the table")
            PopupArea.do("click on the first row of the table")
            PopupArea.do("hover on 'إختر' button")
            PopupArea.do("click on 'إختر' button")

            PopupArea.do("hover on the button of 'من حالة' field ")
            PopupArea.do("click on the button of 'من حالة' field ")
            PopupArea.do("hover on 'بحث' button")
            PopupArea.do("click on 'بحث' button")
            PopupArea.do(f"type {FromStatusCode} into 'الرمز' field")
            PopupArea.do("hover on 'بحث' button inside the box")
            PopupArea.do("click on 'بحث' button inside the box")
            res1 = PopupArea.get("value under 'الرمز' column")
            assert res1 == FromStatusCode , 'From Status Code result is displayed wrongly'
            PopupArea.do("hover on the first row of the table")
            PopupArea.do("click on the first row of the table")
            PopupArea.do("hover on 'إختر' button")
            PopupArea.do("click on 'إختر' button")

            PopupArea.do("hover on the button of 'من منصب' field ")
            PopupArea.do("click on the button of 'من منصب' field ")
            PopupArea.do("hover on 'بحث' button")
            PopupArea.do("click on 'بحث' button")
            PopupArea.do(f"type {FromRole} into 'الرمز' field")
            PopupArea.do("hover on 'بحث' button inside the box")
            PopupArea.do("click on 'بحث' button inside the box")
            res2 = PopupArea.get("value under 'الإسم' column")
            assert res2 == FromRole , 'From Role result is displayed wrongly'
            PopupArea.do("hover on the first row of the table")
            PopupArea.do("click on the first row of the table")
            PopupArea.do("hover on 'إختر' button")
            PopupArea.do("click on 'إختر' button")     

            PopupArea.do("hover on the button of 'إلى حالة' field ")
            PopupArea.do("click on the button of 'إلى حالة' field ")
            PopupArea.do("hover on 'بحث' button")
            PopupArea.do("click on 'بحث' button")
            PopupArea.do(f"type {ToStatusCode} into 'الرمز' field")
            PopupArea.do("hover on 'بحث' button inside the box")
            PopupArea.do("click on 'بحث' button inside the box")
            res3 = PopupArea.get("value under 'الرمز' column")
            assert res3 == ToStatusCode , 'To Status Code result is displayed wrongly'
            PopupArea.do("hover on the first row of the table")
            PopupArea.do("click on the first row of the table")
            PopupArea.do("hover on 'إختر' button")
            PopupArea.do("click on 'إختر' button")  


            PopupArea.do("hover on the button of 'إلى منصب' field ")
            PopupArea.do("click on the button of 'إلى منصب' field ")
            PopupArea.do("hover on 'بحث' button")
            PopupArea.do("click on 'بحث' button")
            PopupArea.do(f"type {ToRole} into 'الرمز' field")
            PopupArea.do("hover on 'بحث' button inside the box")
            PopupArea.do("click on 'بحث' button inside the box")
            res4 = PopupArea.get("value under 'الإسم' column")
            assert res4 == ToRole , 'To Role result is displayed wrongly'
            PopupArea.do("hover on the first row of the table")
            PopupArea.do("click on the first row of the table")
            PopupArea.do("hover on 'إختر' button")
            PopupArea.do("click on 'إختر' button")


            PopupArea.do("hover on the button of 'الحالة الرئيسية' field ")
            PopupArea.do("click on the button of 'الحالة الرئيسية' field ")
            PopupArea.do("hover on 'بحث' button")
            PopupArea.do("click on 'بحث' button")
            PopupArea.do(f"type {MainStatusCode} into 'الرمز' field")
            PopupArea.do("hover on 'بحث' button inside the box")
            PopupArea.do("click on 'بحث' button inside the box")
            res5 = PopupArea.get("value under 'الرمز' column")
            assert res5 == MainStatusCode , 'Main Status Code result is displayed wrongly'
            PopupArea.do("hover on the first row of the table")
            PopupArea.do("click on the first row of the table")
            PopupArea.do("hover on 'إختر' button")
            PopupArea.do("click on 'إختر' button")


            PopupArea.do("hover on 'حفظ' button")

            PopupArea.do(f"hover on {InboxStatus} radio button of 'حالة الصندوق' area")
            PopupArea.do(f"click on {InboxStatus} radio button of 'حالة الصندوق' area")

            PopupArea.do(f"hover on 'نعم' radio button of 'نشط' area")
            PopupArea.do(f"click on 'نعم' radio button of 'نشط' area")

            PopupArea.do("hover on 'حفظ' button")
            PopupArea.do("click on 'حفظ' button")

            print(f"row {i} created successfully ")

        except Exception as e:
            print(f'Row {i} failed: {e}')
            continue
        