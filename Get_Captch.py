import pyautogui
import easyocr as ocr
from pathlib import Path

def get_Captcha():
        #Setup JSON logging
    log_dir=Path("captcha")
    log_dir.mkdir(exist_ok=True)
    # take a screenshot on a location
    im = pyautogui.screenshot(region=(1290,570 ,380,200))
    im.save(rf'captcha\screenshot.png')
    # read the screenshot
    reader = ocr.Reader(['en'], gpu = True)
    result = reader.readtext(rf'captcha\screenshot.png')
    captcha = result[0][1]
    print(captcha)
    return captcha