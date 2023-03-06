from AutoScreen import *
from adbutils import adb
from PIL import Image

import time


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.StreamHandler()])
    logging.info("starts auto screen")
    auto_screen = AutoScreen()
    auto_screen.run()
    auto_screen.close()
    logging.info("ends auto screen")
