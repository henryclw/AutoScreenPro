import logging
import os
import subprocess
from typing import List

from config import Config


class ADBPropertiesHelper:
    @staticmethod
    def run_adb_command(adb_command: str) -> str:
        logging.info("run adb command: %s" % adb_command)
        result = subprocess.run(adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logging.info(f"adb command return with this stdout: {result.stdout.strip()}")
            logging.info(f"adb command return with this stderr: {result.stderr.strip()}")
            return result.stdout.strip()
        else:
            logging.error(f"adb command failed with: {result.stderr.strip()}")
            raise RuntimeError(result.stderr)

    @staticmethod
    def set_show_touches(flag: bool):
        ADBPropertiesHelper.run_adb_command("adb shell settings put system show_touches %s" % ("1" if flag else "0"))

    @staticmethod
    def set_show_pointer_location(flag: bool):
        ADBPropertiesHelper.run_adb_command(
            "adb shell settings put system pointer_location %s" % ("1" if flag else "0"))

    @staticmethod
    def set_show_debug_layout(flag: bool):
        ADBPropertiesHelper.run_adb_command(
            "adb shell setprop debug.layout %s && adb shell service call activity 1599295570" % (
                "true" if flag else "false"))

    @staticmethod
    def list_all_devices() -> List[str]:
        adb_command = "adb devices"
        device_list = []
        result = ADBPropertiesHelper.run_adb_command(adb_command)
        devices = result.split("\n")[1:]
        for d in devices:
            device_list.append(d.split()[0])
        logging.info(f"get android devices: {device_list}")
        return device_list


class AndroidController:
    def __init__(self, device=None):
        config: Config = Config()
        if device is None:
            self.device = ADBPropertiesHelper.list_all_devices()[0]
            logging.info(f"no device provided in AndroidController.__init__, using {self.device}")
        else:
            self.device = device
        self.screenshot_dir = config.android_screenshot_dir
        self.xml_dir = config.android_xml_dir
        self.width, self.height = self.get_device_size()
        self.backslash = "\\"

    def get_device_size(self):
        adb_command = f"adb -s {self.device} shell wm size"
        result = ADBPropertiesHelper.run_adb_command(adb_command)
        return map(int, result.split(": ")[1].split("x"))

    def get_screenshot(self, filename, save_dir):
        cap_command = f"adb -s {self.device} shell screencap -p " \
                      f"{os.path.join(self.screenshot_dir, filename + '.png').replace(self.backslash, '/')}"
        pull_command = f"adb -s {self.device} pull " \
                       f"{os.path.join(self.screenshot_dir, filename + '.png').replace(self.backslash, '/')} " \
                       f"{os.path.join(save_dir, filename + '.png')}"
        delete_file_command = f"adb -s {self.device} shell rm " \
                              f"{os.path.join(self.screenshot_dir, filename + '.png').replace(self.backslash, '/')}"
        ADBPropertiesHelper.run_adb_command(cap_command)
        ADBPropertiesHelper.run_adb_command(pull_command)
        ADBPropertiesHelper.run_adb_command(delete_file_command)
        return os.path.join(save_dir, filename + ".png")

    def get_xml(self, filename, save_dir):
        dump_command = f"adb -s {self.device} shell uiautomator dump --compressed " \
                       f"{os.path.join(self.xml_dir, filename + '.xml').replace(self.backslash, '/')}"
        pull_command = f"adb -s {self.device} pull " \
                       f"{os.path.join(self.xml_dir, filename + '.xml').replace(self.backslash, '/')} " \
                       f"{os.path.join(save_dir, filename + '.xml')}"
        delete_file_command = f"adb -s {self.device} shell rm " \
                              f"{os.path.join(self.xml_dir, filename + '.xml').replace(self.backslash, '/')}"
        ADBPropertiesHelper.run_adb_command(dump_command)
        ADBPropertiesHelper.run_adb_command(pull_command)
        ADBPropertiesHelper.run_adb_command(delete_file_command)
        return os.path.join(save_dir, filename + ".xml")

    def back(self):
        adb_command = f"adb -s {self.device} shell input keyevent KEYCODE_BACK"
        ret = ADBPropertiesHelper.run_adb_command(adb_command)
        return ret

    def tap(self, x, y):
        adb_command = f"adb -s {self.device} shell input tap {x} {y}"
        ret = ADBPropertiesHelper.run_adb_command(adb_command)
        return ret

    def text(self, input_str):
        input_str = input_str.replace(" ", "%s")
        input_str = input_str.replace("'", "")
        adb_command = f"adb -s {self.device} shell input text {input_str}"
        ret = ADBPropertiesHelper.run_adb_command(adb_command)
        return ret

    def long_press(self, x, y, duration=1000):
        adb_command = f"adb -s {self.device} shell input swipe {x} {y} {x} {y} {duration}"
        ret = ADBPropertiesHelper.run_adb_command(adb_command)
        return ret

    def swipe(self, x, y, direction, dist="medium", quick=False):
        unit_dist = int(self.width / 10)
        if dist == "long":
            unit_dist *= 3
        elif dist == "medium":
            unit_dist *= 2
        if direction == "up":
            offset = 0, -2 * unit_dist
        elif direction == "down":
            offset = 0, 2 * unit_dist
        elif direction == "left":
            offset = -1 * unit_dist, 0
        elif direction == "right":
            offset = unit_dist, 0
        else:
            raise RuntimeError(f"Unknown direction: {direction}")
        duration = 100 if quick else 400
        adb_command = f"adb -s {self.device} shell input swipe {x} {y} {x+offset[0]} {y+offset[1]} {duration}"
        ret = ADBPropertiesHelper.run_adb_command(adb_command)
        return ret

    def swipe_precise(self, start, end, duration=400):
        start_x, start_y = start
        end_x, end_y = end
        adb_command = f"adb -s {self.device} shell input swipe {start_x} {start_x} {end_x} {end_y} {duration}"
        ret = ADBPropertiesHelper.run_adb_command(adb_command)
        return ret


class UINode:
    def __init__(self, name, bbox, attrib):
        self.name = name
        self.bbox = bbox
        self.attrib = attrib
