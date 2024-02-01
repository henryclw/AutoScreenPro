import cv2
import logging
import random

from matplotlib.colors import CSS4_COLORS, to_rgb


def add_text_with_transparent_bg(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, text_color=(255, 255, 255), bg_color=(128, 128, 128), alpha=0.5):
    # Calculate text size
    text_size = cv2.getTextSize(text, font, font_scale, 2)[0]
    # Calculate background rectangle coordinates
    x, y = position
    bg_rect_start = (x, y)
    bg_rect_end = (x + text_size[0] + 10, y + text_size[1] + 10)
    # Create overlay for transparency
    overlay = image.copy()
    cv2.rectangle(overlay, bg_rect_start, bg_rect_end, bg_color, -1)
    # Blend image and overlay with transparency
    image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
    # Add text over rectangle
    cv2.putText(image, text, (x + 5, y + 30), font, font_scale, text_color, 2, bottomLeftOrigin=False)
    return image


def draw_bbox_multi(img_path, output_path, elem_list):
    imgcv = cv2.imread(img_path)
    count = 1
    for elem in elem_list:
        try:
            top_left = elem.bbox[0]
            bottom_right = elem.bbox[1]
            left, top = top_left[0], top_left[1]
            right, bottom = bottom_right[0], bottom_right[1]
            label = str(count)
            label = str(elem.name)
            text_color = to_rgb(random.choice(list(CSS4_COLORS.values())))
            text_color = tuple(int(round(c * 255)) for c in text_color)
            rectangle_shrink = 5
            imgcv = add_text_with_transparent_bg(imgcv, label, (left + rectangle_shrink, top + rectangle_shrink), text_color=text_color)
            imgcv = cv2.rectangle(imgcv, (left + rectangle_shrink, top + rectangle_shrink), (right - rectangle_shrink, bottom - rectangle_shrink), text_color, 2)
        except Exception as e:
            logging.error(f"ERROR: An exception occurs while labeling the image\n{e}")
        count += 1
    cv2.imwrite(output_path, imgcv)
    return


class AndroidUIHelper:
    @staticmethod
    def get_box_from_bounds_raw_str(bounds: str):
        bounds = bounds.replace('[', '').replace(']', ',').split(',')
        bounds = map(int, bounds[:4])
        left, high, right, low = bounds
        return left, high, right, low
