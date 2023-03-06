from AutoScreen import AutoScreen
from adbutils import adb
from PIL import Image

import time


if __name__ == "__main__":
    print("hw")
    auto_screen = AutoScreen()

    image = auto_screen.get_last_frame()
    image.save("./data/2.png")
    auto_screen.scroll_down()
    time.sleep(1.2)
    image = auto_screen.get_last_frame()
    image.save("./data/3.png")
    auto_screen.close()
