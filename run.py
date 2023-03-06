from AutoScreen import AutoScreen
from adbutils import adb
from PIL import Image

import scrcpy
import time


if __name__ == "__main__":
    print("hw")
    auto_screen = AutoScreen()

    image = auto_screen.last_frame()
    image.save("./data/2.png")
    auto_screen.scroll()
    time.sleep(1.2)
    image = auto_screen.last_frame()
    image.save("./data/3.png")
    auto_screen.close()
