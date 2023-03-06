from adbutils import adb
from PIL import Image

import scrcpy
import time


class AutoScreen:
    def __init__(self):
        adb.connect("localhost:5555")
        self.client = scrcpy.Client(device=adb.device_list()[0].serial)
        self.client.start(threaded=True, daemon_threaded=True)

        self._frame_ready = False
        self.client.add_listener(scrcpy.EVENT_FRAME, self._frame_is_ready_now)

    def _frame_is_ready_now(self, frame):
        if frame is not None:
            self._frame_ready = True

    def last_frame(self):
        self._frame_ready = False
        while not self._frame_ready:
            time.sleep(0.01)

        rgb = self.client.last_frame[..., ::-1].copy()  # bgr to rgb
        return Image.fromarray(rgb)

    def scroll(self):
        """
        Scroll screen

        Args:
            x: horizontal position
            y: vertical position
            h: horizontal movement
            v: vertical movement
        """
        self.client.control.scroll(500, 500, 0, -3)

    def close(self):
        self.client.stop()

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, move_step_length: int = 5, move_steps_delay: float = 0.005):
        self.client.control.swipe(start_x, start_y, end_x, end_y, move_step_length, move_steps_delay)

    def get_resolution(self) -> (int, int):
        return self.client.resolution
