import logging
import random

from adbutils import adb
from PIL import Image

import scrcpy
import subprocess
import time


class ADBPropertiesHelper:
    @staticmethod
    def run_bash_command(command: str) -> str:
        print(command)
        return subprocess.check_output(command, shell=True)

    @staticmethod
    def set_show_touches(flag: bool):
        ADBPropertiesHelper.run_bash_command("adb shell settings put system show_touches %s" % ("1" if flag else "0"))

    @staticmethod
    def set_show_pointer_location(flag: bool):
        ADBPropertiesHelper.run_bash_command("adb shell settings put system pointer_location %s" % ("1" if flag else "0"))

    @staticmethod
    def set_show_debug_layout(flag: bool):
        ADBPropertiesHelper.run_bash_command(
            "adb shell setprop debug.layout %s && adb shell service call activity 1599295570" % ("true" if flag else "false"))


class ScreenClient:
    def __init__(self):
        adb.connect("localhost:5555")
        self.client = scrcpy.Client(device=adb.device_list()[0].serial)
        self.client.start(threaded=True, daemon_threaded=True)
        logging.info("client start")

        # self.client.control.set_screen_power_mode(scrcpy.POWER_MODE_OFF)
        # logging.info("screen power off")

        self._frame_ready = False
        self.client.add_listener(scrcpy.EVENT_FRAME, self._frame_is_ready_now)

    def __del__(self):
        self.close()

    def _frame_is_ready_now(self, frame):
        if frame is not None:
            self._frame_ready = True

    def get_last_frame(self):
        self._frame_ready = False
        while not self._frame_ready:
            time.sleep(0.01)
        rgb = self.client.last_frame[..., ::-1].copy()  # RGB channels
        return Image.fromarray(rgb)

    def scroll(self, x: int, y: int, h: int, v: int):
        """
        Scroll screen

        Args:
            x: horizontal position
            y: vertical position
            h: horizontal movement
            v: vertical movement
        """
        self.client.control.scroll(x, y, h, v)

    def scroll_down(self):
        x, y = self.get_center_of_screen()
        self.scroll(x, y, 0, -3)

    def close(self):
        self.client.stop()
        logging.info("client closed")

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int,
              move_step_length: int = 5, move_steps_delay: float = 0.005):
        self.client.control.swipe(start_x, start_y, end_x, end_y, move_step_length, move_steps_delay)

    def swipe_down(self):
        x, y = self.get_center_of_screen()
        start_x = x + random.randint(-300, 300)
        end_x = start_x + random.randint(-200, 200)
        start_y = y + random.randint(-100, 700)
        end_y = start_y + random.randint(-900, -200)
        self.swipe(start_x, start_y, end_x, end_y, random.randint(10, 30), random.random() / 10)

    def get_resolution(self) -> (int, int):
        return self.client.resolution

    def get_center_of_screen(self) -> (int, int):
        (x, y) = self.get_resolution()
        return x // 2, y // 2


class AutoScreen:
    def __init__(self):
        self.screen_client = ScreenClient()

    def __del__(self):
        self.close()

    def run(self):
        for i in range(20):
            image = self.screen_client.get_last_frame()
            self.save_image(image)
            self.screen_client.swipe_down()
            time.sleep(random.uniform(0.8, 2.4))

    def save_image(self, image):
        time_stamp = time.time_ns()
        image.save("./data/raw/%d.png" % time_stamp)

    def close(self):
        self.screen_client.close()


