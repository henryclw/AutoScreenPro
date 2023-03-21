import logging
import time
from typing import List

from PIL import Image
from IPython.display import display
from matplotlib import pyplot as plt

import cv2 as cv
import numpy as np
import math

import config


cd = config.Config().config_dict


class ScreenshotProcessor:
    def __init__(self, pil_image: Image):
        self.pil_image = pil_image
        self.image_array = np.asarray(self.pil_image)
        logging.info("ScreenshotProcessor self.image_array.shape is {}".format(self.image_array.shape))

    # def __del__(self):
    #     self.pil_image.close()

    def _get_gray_array(self):
        gray = cv.cvtColor(self.image_array, cv.COLOR_BGR2GRAY)
        logging.info("ScreenshotProcessor Gray array shape is {}".format(gray.shape))
        return gray

    def _get_cut_line_position_by_gray(self, gray: np.ndarray):
        cut_x_list = []
        for i in range(gray.shape[0]):
            # for i in range(1850, 1860):
            this_line = gray[i, :]
            if 226 <= np.median(this_line) <= 229 and this_line.min() > 225 and this_line.max() < 230:
                logging.info("In _get_cut_line_position_by_gray i: {}, max: {}, min: {}, median: {}, mean: {}"
                             .format(i, this_line.max(), this_line.min(), np.median(this_line), this_line.mean()))
                cut_x_list.append(i)
        return cut_x_list

    def _save_first_wechat_moment(self, cut_x_list: List, save_base_path: str):
        time_stamp = time.time_ns()
        this_moment = self.image_array[cut_x_list[0]: cut_x_list[1], :]
        this_moment = Image.fromarray(this_moment)
        # this_moment.save(save_base_path + "s%d.png" % i)
        this_moment.save(save_base_path + "%d.png" % time_stamp)

    def cut_this_wechat_moment(self):
        gray = self._get_gray_array()
        cut_x_list = self._get_cut_line_position_by_gray(gray)
        logging.info("In cut_this_wechat_moment cut_x_list: {}".format(cut_x_list))
        if len(cut_x_list) > 1:
            swipe_down_distance_for_next_moment = cut_x_list[1] - cd["wechat_moment_next_y_head_position"]
            self._save_first_wechat_moment(cut_x_list, cd["wechat_moment_image_save_path"])
        else:
            logging.warning("In cut_this_wechat_moment, cut_x_list length is less than two")
            if len(cut_x_list) == 1:
                swipe_down_distance_for_next_moment = max(cut_x_list[0] - cd["wechat_moment_next_y_head_position"], 960)
            else:
                swipe_down_distance_for_next_moment = 1800
        logging.info("In cut_this_wechat_moment swipe_down_distance_for_next_moment: {}"
                     .format(swipe_down_distance_for_next_moment))
        return swipe_down_distance_for_next_moment


if __name__ == "__main__":
    the_image = Image.open(cd["raw_screen_shot_path"] + "1678168986611948200.png")
    sp = ScreenshotProcessor(the_image)
    sp.cut_this_wechat_moment()
