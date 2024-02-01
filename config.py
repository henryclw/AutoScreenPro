import yaml


class Config:
    def __init__(self):
        with open("config.yaml", "r", encoding="utf-8") as config_file:
            self.config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
        self.raw_screen_shot_path = self.config_dict["raw_screen_shot_path"]
        self.android_screenshot_dir = self.config_dict["ANDROID_SCREENSHOT_DIR"]
        self.android_xml_dir = self.config_dict["ANDROID_XML_DIR"]
        self.min_dist = self.config_dict["MIN_DIST"]
