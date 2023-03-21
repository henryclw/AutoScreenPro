import yaml


class Config:
    def __init__(self):
        with open("config.yaml", "r") as config_file:
            self.config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
        self.raw_screen_shot_path = self.config_dict["raw_screen_shot_path"]
