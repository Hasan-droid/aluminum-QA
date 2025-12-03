import threading
from pathlib import Path
import io
from PIL import Image
import numpy as np
import time
from datetime import datetime
import imageio

class VideoRecording:
    def __init__(self, driver, request):
        self.driver = driver
        self.request = request
        self.frames = []
        self.video_dir = Path("videos")
        self.stop_event = threading.Event()
        self.video_dir.mkdir(exist_ok=True)
        self.target_size = (1920, 1080)
        self.capture_thread = None

    def _capture_loop_thread(self):
        """Continuously capture frames until stopped"""
        frame_count = 0
        while not self.stop_event.is_set():
            try:
                # Get screenshot as PNG bytes
                png_bytes = self.driver.get_screenshot_as_png()
                
                # Convert PNG bytes to PIL Image
                img = Image.open(io.BytesIO(png_bytes))
                
                # Resize to target size to ensure consistency
                img_resized = img.resize(self.target_size, Image.Resampling.LANCZOS)
                
                # Convert PIL Image to numpy array (RGB format)
                img_array = np.array(img_resized)
                
                # Only append if image is valid (has proper dimensions)
                if len(img_array.shape) >= 2:
                    self.frames.append(img_array)
                    frame_count += 1
                    if frame_count % 10 == 0:  # Print every 10 frames
                        print(f"[{self.request.node.name}] Captured {frame_count} frames...")
                else:
                    print(f"[{self.request.node.name}] Invalid frame shape: {img_array.shape}")
            except Exception as e:
                if not self.stop_event.is_set():  # Only print if not stopping
                    print(f"[{self.request.node.name}] Error capturing frame: {e}")
            time.sleep(0.5)  # Capture every 0.5 seconds
    
    def start_capture(self):
        # Start capturing in background thread
        self.capture_thread = threading.Thread(target=self._capture_loop_thread, daemon=True)
        self.capture_thread.start()
        print(f"[{self.request.node.name}] Started video recording")

    def stop_capture(self):
        # Stop capturing
        print(f"[{self.request.node.name}] Stopping video recording...")
        self.stop_event.set()
        if self.capture_thread:
            self.capture_thread.join(timeout=2)  # Wait up to 2 seconds for thread to finish
    
    def save_video(self):
        # Save video
        print(f"[{self.request.node.name}] Captured {len(self.frames)} frames total")
        if self.frames:
            # Filter and validate frames
            valid_frames = []
            for i, frame in enumerate(self.frames):
                if len(frame.shape) >= 2:
                    # Ensure frame is the correct size
                    if frame.shape[:2] != self.target_size[::-1]:  # numpy uses (height, width)
                        # Resize if needed
                        img = Image.fromarray(frame)
                        img_resized = img.resize(self.target_size, Image.Resampling.LANCZOS)
                        frame = np.array(img_resized)
                    valid_frames.append(frame)
                else:
                    print(f"[{self.request.node.name}] Skipping invalid frame {i}: shape {frame.shape}")
            
            print(f"[{self.request.node.name}] Valid frames: {len(valid_frames)}")
            
            if valid_frames:
                # Verify all frames have the same size
                first_size = valid_frames[0].shape[:2]
                consistent_frames = [f for f in valid_frames if f.shape[:2] == first_size]
                
                if len(consistent_frames) != len(valid_frames):
                    print(f"[{self.request.node.name}] ⚠ Some frames had inconsistent sizes, using {len(consistent_frames)} consistent frames")
                
                if consistent_frames:
                    test_name = self.request.node.name.replace("::", "_").replace("/", "_")

                    scenario_num=None;
                    for marker in self.request.node.iter_markers():
                        if marker.name.startswith("scenario"):
                            scenario_num = marker.name.replace("scenario", "")
                            break
                    worker_suffix = f"_CaseScenario{scenario_num}" if scenario_num else ""
                    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                    video_path = self.video_dir / f"{test_name}{worker_suffix}_{date_str}.mp4"
                    try:
                        print(f"[{self.request.node.name}] Saving video to {video_path}...")
                        print(f"[{self.request.node.name}] Frame size: {consistent_frames[0].shape}, Count: {len(consistent_frames)}")
                        imageio.mimsave(str(video_path), consistent_frames, fps=2, codec='libx264')
                        print(f"[{self.request.node.name}] ✓ Video saved: {video_path}")
                    except Exception as e:
                        print(f"[{self.request.node.name}] ✗ Failed to save video: {e}")
                        import traceback
                        traceback.print_exc()
                else:
                    print(f"[{self.request.node.name}] ⚠ No consistent frames to save!")
            else:
                print(f"[{self.request.node.name}] ⚠ No valid frames to save!")
        else:
            print(f"[{self.request.node.name}] ⚠ No frames captured!")