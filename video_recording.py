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
        """
        `driver` can be a single Selenium WebDriver instance or
        an iterable of WebDriver instances (multi‑browser capture).
        """
        # Normalize to a list of drivers so we can support multi‑browser
        if isinstance(driver, (list, tuple)):
            self.drivers = list(driver)
        else:
            self.drivers = [driver]

        self.request = request
        # Frames are stored per browser index for multi‑browser support
        # {browser_index: [np.ndarray, ...]}
        self.frames_by_browser = {i: [] for i in range(len(self.drivers))}

        self.video_dir = Path("videos")
        self.stop_event = threading.Event()
        self.video_dir.mkdir(exist_ok=True)
        self.target_size = (1920, 1080)
        self.capture_thread = None

    def _capture_loop_thread(self):
        """Continuously capture frames until stopped"""
        frame_counts = {i: 0 for i in range(len(self.drivers))}

        # Target a higher capture frequency (more FPS in output video)
        # Previous value was 0.5s (≈2 FPS). Use 0.1s for up to ~10 FPS.
        capture_interval = 0.1

        while not self.stop_event.is_set():
            for idx, drv in enumerate(self.drivers):
                try:
                    # Get screenshot as PNG bytes
                    png_bytes = drv.get_screenshot_as_png()

                    # Convert PNG bytes to PIL Image
                    img = Image.open(io.BytesIO(png_bytes))

                    # Resize to target size to ensure consistency
                    img_resized = img.resize(self.target_size, Image.Resampling.LANCZOS)

                    # Convert PIL Image to numpy array (RGB format)
                    img_array = np.array(img_resized)

                    # Only append if image is valid (has proper dimensions)
                    if len(img_array.shape) >= 2:
                        self.frames_by_browser[idx].append(img_array)
                        frame_counts[idx] += 1
                        if frame_counts[idx] % 10 == 0:  # Print every 10 frames per browser
                            print(
                                f"[{self.request.node.name}][browser {idx+1}] "
                                f"Captured {frame_counts[idx]} frames..."
                            )
                    else:
                        print(
                            f"[{self.request.node.name}][browser {idx+1}] "
                            f"Invalid frame shape: {img_array.shape}"
                        )
                except Exception as e:
                    if not self.stop_event.is_set():  # Only print if not stopping
                        print(
                            f"[{self.request.node.name}][browser {idx+1}] "
                            f"Error capturing frame: {e}"
                        )

            time.sleep(capture_interval)
    
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
        # Save video(s) – one per browser instance if multiple drivers were provided
        total_frames = sum(len(frames) for frames in self.frames_by_browser.values())
        print(f"[{self.request.node.name}] Captured {total_frames} frames total")

        if total_frames == 0:
            print(f"[{self.request.node.name}] ⚠ No frames captured!")
            return

        test_name = self.request.node.name.replace("::", "_").replace("/", "_")

        scenario_num = None
        for marker in self.request.node.iter_markers():
            if marker.name.startswith("scenario"):
                scenario_num = marker.name.replace("scenario", "")
                break

        worker_suffix = f"_CaseScenario{scenario_num}" if scenario_num else ""
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Match FPS to the higher capture rate – aim for 10 FPS
        target_fps = 10

        for browser_idx, frames in self.frames_by_browser.items():
            if not frames:
                print(
                    f"[{self.request.node.name}][browser {browser_idx+1}] "
                    f"⚠ No frames to save!"
                )
                continue

            # Filter and validate frames
            valid_frames = []
            for i, frame in enumerate(frames):
                if len(frame.shape) >= 2:
                    # Ensure frame is the correct size
                    if frame.shape[:2] != self.target_size[::-1]:  # numpy uses (height, width)
                        # Resize if needed
                        img = Image.fromarray(frame)
                        img_resized = img.resize(self.target_size, Image.Resampling.LANCZOS)
                        frame = np.array(img_resized)
                    valid_frames.append(frame)
                else:
                    print(
                        f"[{self.request.node.name}][browser {browser_idx+1}] "
                        f"Skipping invalid frame {i}: shape {frame.shape}"
                    )

            print(
                f"[{self.request.node.name}][browser {browser_idx+1}] "
                f"Valid frames: {len(valid_frames)}"
            )

            if not valid_frames:
                print(
                    f"[{self.request.node.name}][browser {browser_idx+1}] "
                    f"⚠ No valid frames to save!"
                )
                continue

            # Verify all frames have the same size
            first_size = valid_frames[0].shape[:2]
            consistent_frames = [f for f in valid_frames if f.shape[:2] == first_size]

            if len(consistent_frames) != len(valid_frames):
                print(
                    f"[{self.request.node.name}][browser {browser_idx+1}] "
                    f"⚠ Some frames had inconsistent sizes, using {len(consistent_frames)} consistent frames"
                )

            if not consistent_frames:
                print(
                    f"[{self.request.node.name}][browser {browser_idx+1}] "
                    f"⚠ No consistent frames to save!"
                )
                continue

            # For multi‑browser we suffix the filename per browser to keep videos separate
            browser_suffix = (
                f"_browser{browser_idx+1}" if len(self.frames_by_browser) > 1 else ""
            )
            video_path = (
                self.video_dir
                / f"{test_name}{worker_suffix}{browser_suffix}_{date_str}.mp4"
            )

            try:
                print(
                    f"[{self.request.node.name}][browser {browser_idx+1}] "
                    f"Saving video to {video_path}..."
                )
                print(
                    f"[{self.request.node.name}][browser {browser_idx+1}] "
                    f"Frame size: {consistent_frames[0].shape}, "
                    f"Count: {len(consistent_frames)}, FPS: {target_fps}"
                )
                imageio.mimsave(
                    str(video_path), consistent_frames, fps=target_fps, codec="libx264"
                )
                print(
                    f"[{self.request.node.name}][browser {browser_idx+1}] "
                    f"✓ Video saved: {video_path}"
                )
            except Exception as e:
                print(
                    f"[{self.request.node.name}][browser {browser_idx+1}] "
                    f"✗ Failed to save video: {e}"
                )
                import traceback

                traceback.print_exc()