import time
from PySide6.QtCore import QTimer
#import imageio
import numpy as np

class ScreenRecorder:
    def __init__(self, window, fps=30):
        self.window = window
        self.output_file = f"records/{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}.mp4"
        self.fps = fps
        self.frames_count = 0
        self.writer = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.capture_frame)
        self.start_time = None

    def start_recording(self):
        self.writer = imageio.get_writer(self.output_file, fps=self.fps, macro_block_size=1)
        self.start_time = time.time()
        self.timer.start(1000 / self.fps)

    def capture_frame(self):
        pixmap = self.window.grab()
        image = pixmap.toImage()
        buffer = bytes(image.bits())
        img = np.frombuffer(buffer, dtype=np.uint8).reshape((image.height(), image.width(), 4))
        img = img[:, :, :3]
        img = img[..., ::-1]
        self.writer.append_data(img)
        self.frames_count += 1


    def stop_recording(self):
        self.timer.stop()
        self.writer.close()
        print(f"Recording stopped. Total frames captured: {self.frames_count}")