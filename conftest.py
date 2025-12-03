import os
from pathlib import Path
from video_recording import VideoRecording


os.environ['ALUMNIUM_MODEL'] = 'ollama/llama3.1:70b'
os.environ['ALUMNIUM_OLLAMA_URL'] = 'http://192.168.6.177:11435'
os.environ['ALUMNIUM_CACHE'] = 'filesystem'

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from alumnium import Alumni
from pytest import fixture
import time
from pytest import hookimpl


# Register custom markers for scenario 1 and scenario 2
def pytest_configure(config):
    config.addinivalue_line("markers", "scenario1: Run test in scenario 1")
    config.addinivalue_line("markers", "scenario2: Run test in scenario 2")

@fixture(scope="session", autouse=True)
def cleanup_videos():
    """Delete all videos at the start of test session"""
    video_dir = Path("videos")
    video_dir.mkdir(exist_ok=True)  # Create directory first
    
    # Delete all files in the directory
    if video_dir.exists():
        print("Cleaning up videos directory...")
        for file in video_dir.glob("*"):
            try:
                if file.is_file():
                    file.unlink()
            except Exception as e:
                print(f"Warning: Could not delete {file}: {e}")
    yield

@fixture(scope="function")
def driver(request):
    chrome_options = Options()
    # Specify Chromium binary path (since it's installed via snap)
    chrome_options.binary_location = "/snap/bin/chromium"
    
    # CRITICAL: Required for WSL2/headless environments to fix DevToolsActivePort error
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    # Use unique remote debugging port per worker to avoid conflicts
    import os 
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", 'gw0')
    port = 9222 + hash(worker_id) % 1000 #Generate a unique port for each worker
    
    # Optional: Use headless mode (remove if you want to see the browser)
    # chrome_options.add_argument('--headless=new')
    
    # Optional: Set remote debugging port (can help with DevTools issues)
    chrome_options.add_argument(f'--remote-debugging-port={port}')
    
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

    # Set a fixed window size to ensure consistent screenshots
    driver.set_window_size(1920, 1080)
    
    video_recording = VideoRecording(driver, request)
    
    video_recording.start_capture()

    yield driver

    video_recording.stop_capture()
    video_recording.save_video()
    
    

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


@fixture(scope="function")
def al(driver: Chrome):
    al = Alumni(driver)
    yield al
    al.quit()
