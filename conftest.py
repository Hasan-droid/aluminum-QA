import os
from pathlib import Path
from video_recording import VideoRecording
import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime
import traceback
import json

_log_entries = []
# Configure to use Ollama instead of OpenAI - MUST be set before importing alumnium
# Using custom Ollama server at http://192.168.6.177:11435
# Model: mistral-small3.1:24b
os.environ['ALUMNIUM_MODEL'] = 'ollama/qwen3-vl:32b'
os.environ['ALUMNIUM_OLLAMA_URL'] = 'http://192.168.6.177:11435'


# os.environ['ALUMNIUM_MODEL'] = 'openai'
# os.environ['OPENAI_API_KEY'] = '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'

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


# Register custom markers for scenario 1 and scenario 2
def pytest_configure(config):
    config.addinivalue_line("markers", "scenario1: Run test in scenario 1")
    config.addinivalue_line("markers", "scenario2: Run test in scenario 2")

    #Setup JSON logging
    log_dir=Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger=logging.getLogger("test_cases_automation")
    logger.setLevel(logging.INFO)

    #Remove existing handlers
    logger.handlers.clear()

    #Custom handler that collects logs in memory
    class ListHandler(logging.Handler):
        def emit(self, record):
            formatter=jsonlogger.JsonFormatter()
            log_entry = json.loads(formatter.format(record))
            _log_entries.append(log_entry)

    list_handler=ListHandler()
    logger.addHandler(list_handler)

    #Console handler for immdiate output
    console_handler=logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(console_handler)

    
    # Store log file path and start time for report
    config._log_file = log_dir / f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    config._test_start_time = datetime.now()

    return logger



# Write JSON array wrapped in report at the end of test session
def pytest_sessionfinish(session, exitstatus):
    """Write all collected logs as a JSON array wrapped in a report"""
    log_file = getattr(session.config, '_log_file', None)
    start_time = getattr(session.config, '_test_start_time', datetime.now())
    
    if log_file and _log_entries:
        # Create report structure with metadata and logs array
        report = {
            "test_run": {
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "total_tests": len(_log_entries),
                "passed": len([e for e in _log_entries if e.get("status") == "passed"]),
                "failed": len([e for e in _log_entries if e.get("status") == "failed"]),
                "skipped": len([e for e in _log_entries if e.get("status") == "skipped"]),
                "exit_status": exitstatus
            },
            "logs": _log_entries  # Array of all log entries
        }
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Test report saved to {log_file}")
            print(f"  Total: {report['test_run']['total_tests']}, "
                  f"Passed: {report['test_run']['passed']}, "
                  f"Failed: {report['test_run']['failed']}, "
                  f"Skipped: {report['test_run']['skipped']}")
        except Exception as e:
            print(f"\n✗ Failed to save report: {e}")

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
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    #Get logger from logging module
    logger=logging.getLogger("test_cases_automation")

    print("Running cache")
    if report.when == "call":
        # Assuming `al` is an instance of `Alumni`.
        al = item.funcargs["al"]
        driver = item.funcargs.get("driver")

        #Extract test information for logging
        test_name=item.nodeid
        scenario=None;
        for marker in item.iter_markers():
            if marker.name.startswith("scenario"):
                scenario=marker.name.replace("scenario", "")
                break
        current_url=None;
        page_title=None;
        if driver:
            try:
                current_url=driver.current_url
                page_title=driver.title
            except:
                pass

        #Log test result
        if report.passed:
            al.cache.save()
            logger.info("Test passed", extra={
                "test_name": test_name,
                "scenario": scenario,
                "status": "passed",
                "duration": f"{report.duration:.2f}s",
                "when": report.when,
                "url": current_url,
                "page_title": page_title
            })
            print("doc saved")
        elif report.failed:
            al.cache.discard()
            
            #Extract error details
            error_type=None;
            error_message=None;
            error_traceback=None;

            if call.excinfo:
                error_type = call.excinfo.typename
                error_message = str(call.excinfo.value) if call.excinfo.value else None
                # Get formatted traceback
                error_traceback = ''.join(traceback.format_exception(
                    call.excinfo.type,
                    call.excinfo.value,
                    call.excinfo.tb
                ))

                    # Log failure with comprehensive details
            logger.error("Test failed", extra={
                "test_name": test_name,
                "scenario": scenario,
                "status": "failed",
                "duration": f"{report.duration:.2f}s",
                "when": report.when,
                "error_type": error_type,
                "error_message": error_message,
                "error_traceback": error_traceback,
                "url": current_url,
                "page_title": page_title,
                "longrepr": str(report.longrepr) if report.longrepr else None
            }, exc_info=call.excinfo)
            
        elif report.skipped:
            logger.warning("Test skipped", extra={
                "test_name": test_name,
                "scenario": scenario,
                "status": "skipped",
                "reason": str(report.longrepr) if report.longrepr else "Unknown reason",
                "when": report.when
            })




@fixture(scope="function")
def al(driver: Chrome):
    al = Alumni(driver)
    yield al
    al.quit()
