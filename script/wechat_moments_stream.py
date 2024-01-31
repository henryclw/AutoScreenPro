import cv2
import logging
import os
import shutil
import time
import xml.etree.ElementTree as ET

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from AutoScreen.DataIOHelper import MinioHelper, PostgresqlHelper
from AutoScreen.utils import draw_bbox_multi, AndroidUIHelper
from AutoScreen.AndroidScreen import AndroidController, UINode


@dataclass
class WechatMomentStream:
    create_time: datetime
    username: str = ""
    body_text: str = ""
    share_link_title: str = ""
    folded_text: str = ""
    picture_list: List[str] = field(default_factory=list)
    liked_users: List[str] = field(default_factory=list)
    comments: List[str] = field(default_factory=list)
    extra_text_clickable: List[str] = field(default_factory=list)
    extra_text_non_clickable: List[str] = field(default_factory=list)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # logging.debug("testing")

    temp_data_base_dir = os.path.join("data", "temp")
    shutil.rmtree(temp_data_base_dir)
    os.makedirs(temp_data_base_dir)

    minio_helper = MinioHelper(bucket_name="asp.wechat.moment.stream")
    postgresql_helper = PostgresqlHelper()
    for round_count in range(10):
        logging.info(f"\n\n---\n\ngetting wechat moment round_count {round_count}")
        # try to get screenshot and ui xml
        for _ in range(3):
            try:
                android_controller = AndroidController()
                screenshot_raw_path = android_controller.get_screenshot("wechat_moment", temp_data_base_dir)
                xml_raw_path = android_controller.get_xml("wechat_moment", temp_data_base_dir)
                logging.info(f"Successfully saved screenshot and ui xml for {android_controller.device}")
                break
            except RuntimeError as e:
                android_controller.reopen_app_by_going_to_homescreen()
        # display(Image(screenshot_raw_path))

        # parse xml tree
        tree = ET.parse(xml_raw_path)
        ui_node_list = []
        for ele in tree.iter():
            if ele.attrib.get("clickable", "false") == "true":
                # if ele.attrib.get("clickable", "false") == "true" or ele.attrib.get("focusable", "false") == "true":
                left, high, right, low = AndroidUIHelper.get_box_from_bounds_raw_str(bounds=ele.attrib.get("bounds"))
                name = ele.attrib.get("resource-id", "no-resource-id").split('/')[-1]
                if name is None:
                    name = ele.attrib.get("content-desc", "no-content-desc")
                ui_node_list.append(UINode(name, ((left, high), (right, low)), ele.attrib))

        # draw parsed nodes on the screenshot
        draw_bbox_multi(screenshot_raw_path, temp_data_base_dir + "/with_box.png", ui_node_list)
        # display(Image(temp_data_base_dir + "/with_box.png"))

        # get moment list
        moment_node_list = tree.findall(".//*[@resource-id='com.tencent.mm:id/n9a']") + tree.findall(
            ".//*[@resource-id='com.tencent.mm:id/n9e']")
        logging.info(f"found {len(moment_node_list)} n9a / n9e node")
        if len(moment_node_list) == 0:
            logging.error("no moment found, try reopen_app_by_going_to_homescreen...")
            android_controller.reopen_app_by_going_to_homescreen()
            continue

        # get the first good moment
        this_moment_low = None
        this_moment_node = None
        for i, moment_node_i in enumerate(moment_node_list):
            left, high, right, low = AndroidUIHelper.get_box_from_bounds_raw_str(bounds=moment_node_i.attrib.get("bounds"))
            # logging.info("this_moment_node is with a high that is too small, skipping it.")
            logging.info(f"moment node {i}, high={high}, low={low}")
            if high > 192 and low < 1918:
                logging.info(f"choosing moment node {i}, with all the box visible")
                this_moment_low = low
                this_moment_node = moment_node_i
                break
        if this_moment_low is None or this_moment_node is None:
            logging.warning("no suitable moment found, skip this round and swipe up a little bit")
            android_controller.swipe_up(200)
            continue

        # save this moment raw data
        this_moment_tree = ET.ElementTree(this_moment_node)
        this_moment_tree.write(temp_data_base_dir + "/this_moment_tree.xml")

        this_moment_is_ad = False
        wechat_moment_stream = WechatMomentStream(create_time=datetime.now())
        # parse node one by one, by its type
        for i, node in enumerate(this_moment_tree.iter()):
            resource_id = node.attrib.get("resource-id", "no-resource-id")
            content_desc = node.attrib.get("content-desc", "no-content-desc")
            text = node.attrib.get("text", "no-text")
            left, high, right, low = AndroidUIHelper.get_box_from_bounds_raw_str(bounds=node.attrib.get("bounds"))
            logging.debug(f"itering within child nodes, {i}, {content_desc}, {text}, {left}, {high}, {right}, {low}")
            if resource_id == "com.tencent.mm:id/n9a":
                logging.debug(f"skipping this node {i}, it's a n9a, 朋友圈主node")
            elif resource_id == "com.tencent.mm:id/n9e":
                logging.debug(f"skipping this node {i}, it's a n9e, 朋友圈主node")
            elif resource_id == "com.tencent.mm:id/od":
                this_avatar_image = cv2.imread(screenshot_raw_path)[high:low, left:right]
                cv2.imwrite(temp_data_base_dir + "/this_avatar_image.png", this_avatar_image)
                # display(Image(temp_data_base_dir + "/this_avatar_image.png"))
                logging.info(f"found od, left={left}, right={right}, high={high}, low={low}")
            elif "图片第" in content_desc:
                # print(left, right, high, low)
                logging.info(f"found picture, left={left}, right={right}, high={high}, low={low}")
                android_controller.tap_in_box(left=left, high=high, right=right, low=low)  # open the picture
                try:
                    time.sleep(5)  # make sure the picture is loaded
                    android_controller.long_press(android_controller.width // 2, android_controller.height // 2)
                    picture_xml_path = android_controller.get_xml("wechat_moment_picture",
                                                                  temp_data_base_dir)  # save the ui xml
                    picture_tree = ET.parse(picture_xml_path)
                    save_node = picture_tree.find(".//*[@text='保存图片']")
                    left, high, right, low = AndroidUIHelper.get_box_from_bounds_raw_str(
                        bounds=save_node.attrib.get("bounds"))
                    android_controller.tap_in_box(left=left, high=high, right=right, low=low)  # click save
                    time.sleep(1)  # make sure the picture is saved
                    this_picture_path = android_controller.copy_and_remove_the_latest_file("/sdcard/Pictures/WeiXin",
                                                                                           temp_data_base_dir)
                    logging.info(f"saved picture to host, this_picture_path={this_picture_path}")
                    this_picture_filename = this_picture_path.split('/')[-1].split('\\')[-1]
                    # print(this_picture_filename)
                    minio_helper.put_object(this_picture_path, this_picture_filename)
                    wechat_moment_stream.picture_list.append(this_picture_filename)
                    os.remove(this_picture_path)
                except Exception as e:
                    logging.warning(f"saved picture error: {e}")
                    pass
                finally:
                    android_controller.press_back_key()
            elif resource_id == "com.tencent.mm:id/n96":
                n96 = text
                if len(n96) > 0:
                    # print(n96)
                    wechat_moment_stream.folded_text = n96
                    logging.info(f"found n96, 被折叠的朋友圈 is {n96}")
                else:
                    logging.debug(f"skipping this node {i}, it's a n96 and length is 0, 被折叠的朋友圈")
            elif resource_id == "com.tencent.mm:id/kbq":
                kbq = text
                # print(kbq)
                wechat_moment_stream.username = kbq
                logging.info(f"found kbq, user is {kbq}")
            elif resource_id == "com.tencent.mm:id/h9t":
                logging.debug(f"skipping this node {i}, it's a h9t, odj的父节点")
            elif resource_id == "com.tencent.mm:id/odj":
                odj = text
                # print(odj)
                wechat_moment_stream.share_link_title = odj
                logging.info(f"found odj, 分享链接标题 is {odj}")
            elif resource_id == "com.tencent.mm:id/cuf" or resource_id == "com.tencent.mm:id/cut":
                cuf_cut = text
                if len(cuf_cut) > 0:
                    # print(cuf_cut)
                    wechat_moment_stream.body_text = cuf_cut
                    logging.info(f"found cuf_cut, 朋友圈内容文字 is {cuf_cut}")
                else:
                    logging.debug(f"skipping this node {i}, it's a cuf / cut and length is 0")
            elif resource_id == "com.tencent.mm:id/r2":
                logging.debug(f"skipping this node {i}, it's a r2, 评论区图标")
            elif resource_id == "com.tencent.mm:id/hbr":
                logging.debug(f"skipping this node {i}, it's a hbr, 点赞区图标")
            elif resource_id == "com.tencent.mm:id/n9v":
                n9v = text
                # print(n9v)
                wechat_moment_stream.liked_users.append(n9v)
                logging.info(f"found cut, 点赞的人 is {n9v}")
            elif resource_id == "com.tencent.mm:id/c6p":
                c6p = text
                # print(c6p)
                wechat_moment_stream.comments.append(c6p)
                logging.info(f"found c6p, 此条评论 is {c6p}")
            elif text is not None and len(text) > 0:
                if node.attrib.get("clickable", "false") == "true":
                    logging.info(f"found extra text, maybe location, text is {text}")
                    if text == "广告":
                        this_moment_is_ad = True
                        logging.warning(f"found out this is ad")
                    else:
                        wechat_moment_stream.extra_text_clickable.append(text)
                else:
                    wechat_moment_stream.extra_text_non_clickable.append(text)
                    logging.info(f"found extra text, maybe a datetime or location, text is {text}")
            else:
                logging.debug(f"ignoring this node, {i}, {node.attrib}")

        if this_moment_is_ad:  # skip saving for ads
            continue
        else:
            print(wechat_moment_stream)
            postgresql_helper.wechat_moment_stream_insert(wechat_moment_stream)
            logging.info(f"saved to database, {wechat_moment_stream}")

        # next swipe up
        next_swipe_up_distance = this_moment_low - 240
        logging.info(f"finished this moment, moving to the next one, next_swipe_up_distance={next_swipe_up_distance}")

        android_controller.swipe_up(next_swipe_up_distance)

    logging.warning("\n\n---\n\nprogam exit")
