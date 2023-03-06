from adbutils import adb
from PIL import Image

import scrcpy
import time


if __name__ == "__main__":
    print("hw")
    adb.connect("127.0.0.1:5555")
    client = scrcpy.Client(device=adb.device_list()[0].serial)
    client.start(threaded=True, daemon_threaded=True)
    # client.control.set_screen_power_mode(scrcpy.POWER_MODE_OFF)
    while client.last_frame is None:
        time.sleep(0.01)
        print("sleep 0.01s")
    print(client.last_frame.shape)

    rgb = client.last_frame[..., ::-1].copy()  # bgr to rgb
    image = Image.fromarray(rgb)
    image.save("./data/2.png")
    client.control.scroll(500, 500, 0, -3)

    time.sleep(1.2)
    rgb = client.last_frame[..., ::-1].copy()  # bgr to rgb
    image = Image.fromarray(rgb)
    image.save("./data/3.png")
    client.stop()
