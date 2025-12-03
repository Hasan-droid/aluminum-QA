import os

# Configure to use Ollama instead of OpenAI - MUST be set before importing alumnium
# Using custom Ollama server at http://192.168.6.177:11435
# Model: mistral-small3.1:24b
# os.environ['ALUMNIUM_MODEL'] = 'ollama/llama3.1:70b'
# os.environ['ALUMNIUM_OLLAMA_URL'] = 'http://192.168.6.177:11435'


os.environ['ALUMNIUM_MODEL'] = 'openai'
os.environ['OPENAI_API_KEY'] = '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'

# Native client expects the base Ollama URL (without /api/generate) so the server can
# append the correct endpoint internally.

os.environ['ALUMNIUM_CACHE'] = 'filesystem'
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from alumnium import Alumni
from pytest import fixture
import time
from pytest import hookimpl




@fixture
def driver():
    chrome_options = Options()
    # Specify Chromium binary path (since it's installed via snap)
    chrome_options.binary_location = "/snap/bin/chromium"
    
    # CRITICAL: Required for WSL2/headless environments to fix DevToolsActivePort error
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # Optional: Use headless mode (remove if you want to see the browser)
    # chrome_options.add_argument('--headless=new')
    
    # Optional: Set remote debugging port (can help with DevTools issues)
    chrome_options.add_argument('--remote-debugging-port=9222')
    
    # Your existing security/SSL options
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    
    # Window size for consistent rendering
    chrome_options.add_argument('--window-size=1920,1080')
    
    chrome_prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_protection_enabled": False,
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)
    
    # Use Selenium Manager (built into Selenium 4.11+) - automatically handles ChromeDriver
    # It will detect Chromium version 142 and download matching ChromeDriver
    driver = Chrome(options=chrome_options)
    yield driver
    driver.quit()

@hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    print("Running cache")
    if report.when == "call":
        # Assuming `al` is an instance of `Alumni`.
        al = item.funcargs["al"]
        if report.passed:
            al.cache.save()
            print("doc saved")
        else:
            al.cache.discard()
            print("doc not saved")


@fixture
def al(driver: Chrome):
    al = Alumni(driver)
    yield al
    al.quit()
