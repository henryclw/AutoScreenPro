from AutoScreen import *
from adbutils import adb
from PIL import Image

import signal
import subprocess
import time

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.StreamHandler()])

    bashCommand = "D:\\path\\scrcpy\\scrcpy.exe --disable-screensaver -w -S -t --power-off-on-close"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    logging.info("starts scrcpy")

    logging.info("starts auto screen")
    auto_screen = AutoScreen()
    auto_screen.run()
    auto_screen.close()
    logging.info("ends auto screen")

    process.send_signal(signal.CTRL_C_EVENT)
    process.terminate()
    logging.info("ends scrcpy")


