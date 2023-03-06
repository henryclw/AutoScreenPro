import os

from AutoScreen import *
from adbutils import adb
from PIL import Image

import signal
import subprocess
import time

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.StreamHandler()])
    logging.info("starts auto screen")
    # auto_screen = AutoScreen()
    # auto_screen.run()
    # auto_screen.close()

    # output = subprocess.check_output("scrcpy --disable-screensaver -w -S -t --power-off-on-close", shell=True)


    bashCommand = "D:\\path\\scrcpy\\scrcpy.exe --disable-screensaver -w -S -t --power-off-on-close"
    # bashCommand = "scrcpy --disable-screensaver -w -S -t --power-off-on-close"
    # bashCommand = "echo %PATH%"
    # Run adb command and capture stdout and stderr output
    print(['cmd', '/c'] + bashCommand.split())
    # process = subprocess.Popen(['cmd', '/c'] + bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # os.set_blocking(process.stdout.fileno(), False)
    print("1")
    logging.info("Sleep started")
    time.sleep(5)
    logging.info("Sleep finished")
    process.send_signal(signal.CTRL_C_EVENT)
    process.terminate()
    logging.info("ends auto screen")
