import os
from pathlib import Path
import imageio
import threading
import time
from PIL import Image
import io
import numpy as np
from datetime import datetime
import shutil

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
    



    # Video recording setup
    frames = []
    video_dir = Path("videos")
    stop_capture = threading.Event()
    capture_thread = None
    target_size = (1920, 1080)  # Fixed target size for all frames

    def capture_loop():
        """Continuously capture frames until stopped"""
        frame_count = 0
        while not stop_capture.is_set():
            try:
                # Get screenshot as PNG bytes
                png_bytes = driver.get_screenshot_as_png()
                
                # Convert PNG bytes to PIL Image
                img = Image.open(io.BytesIO(png_bytes))
                
                # Resize to target size to ensure consistency
                img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                
                # Convert PIL Image to numpy array (RGB format)
                img_array = np.array(img_resized)
                
                # Only append if image is valid (has proper dimensions)
                if len(img_array.shape) >= 2:
                    frames.append(img_array)
                    frame_count += 1
                    if frame_count % 10 == 0:  # Print every 10 frames
                        print(f"[{request.node.name}] Captured {frame_count} frames...")
                else:
                    print(f"[{request.node.name}] Invalid frame shape: {img_array.shape}")
            except Exception as e:
                if not stop_capture.is_set():  # Only print if not stopping
                    print(f"[{request.node.name}] Error capturing frame: {e}")
            time.sleep(0.5)  # Capture every 0.5 seconds
    
    # Start capturing in background thread
    capture_thread = threading.Thread(target=capture_loop, daemon=True)
    capture_thread.start()
    print(f"[{request.node.name}] Started video recording")
    
    yield driver

    # Stop capturing
    print(f"[{request.node.name}] Stopping video recording...")
    stop_capture.set()
    capture_thread.join(timeout=2)  # Wait up to 2 seconds for thread to finish
    
    # Save video
    print(f"[{request.node.name}] Captured {len(frames)} frames total")
    if frames:
        # Filter and validate frames
        valid_frames = []
        for i, frame in enumerate(frames):
            if len(frame.shape) >= 2:
                # Ensure frame is the correct size
                if frame.shape[:2] != target_size[::-1]:  # numpy uses (height, width)
                    # Resize if needed
                    img = Image.fromarray(frame)
                    img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                    frame = np.array(img_resized)
                valid_frames.append(frame)
            else:
                print(f"[{request.node.name}] Skipping invalid frame {i}: shape {frame.shape}")
        
        print(f"[{request.node.name}] Valid frames: {len(valid_frames)}")
        
        if valid_frames:
            # Verify all frames have the same size
            first_size = valid_frames[0].shape[:2]
            consistent_frames = [f for f in valid_frames if f.shape[:2] == first_size]
            
            if len(consistent_frames) != len(valid_frames):
                print(f"[{request.node.name}] ⚠ Some frames had inconsistent sizes, using {len(consistent_frames)} consistent frames")
            
            if consistent_frames:
                test_name = request.node.name.replace("::", "_").replace("/", "_")

                scenario_num=None;
                for marker in request.node.iter_markers():
                    if marker.name.startswith("scenario"):
                        scenario_num = marker.name.replace("scenario", "")
                        break
                worker_suffix = f"_CaseScenario{scenario_num}" if scenario_num else ""
                date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_path = video_dir / f"{test_name}{worker_suffix}_{date_str}.mp4"
                try:
                    print(f"[{request.node.name}] Saving video to {video_path}...")
                    print(f"[{request.node.name}] Frame size: {consistent_frames[0].shape}, Count: {len(consistent_frames)}")
                    imageio.mimsave(str(video_path), consistent_frames, fps=2, codec='libx264')
                    print(f"[{request.node.name}] ✓ Video saved: {video_path}")
                except Exception as e:
                    print(f"[{request.node.name}] ✗ Failed to save video: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"[{request.node.name}] ⚠ No consistent frames to save!")
        else:
            print(f"[{request.node.name}] ⚠ No valid frames to save!")
    else:
        print(f"[{request.node.name}] ⚠ No frames captured!")

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
