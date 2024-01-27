import base64
import cv2
import pyshine as ps
import random

from colorama import Fore, Style
from matplotlib.colors import CSS4_COLORS, to_rgb, cnames


import cv2
import numpy as np

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
    cv2.putText(image, text, (x + 5, y + 25), font, font_scale, text_color, 2, bottomLeftOrigin=False)

    return image


def print_with_color(text: str, color=""):
    if color == "red":
        print(Fore.RED + text)
    elif color == "green":
        print(Fore.GREEN + text)
    elif color == "yellow":
        print(Fore.YELLOW + text)
    elif color == "blue":
        print(Fore.BLUE + text)
    elif color == "magenta":
        print(Fore.MAGENTA + text)
    elif color == "cyan":
        print(Fore.CYAN + text)
    elif color == "white":
        print(Fore.WHITE + text)
    elif color == "black":
        print(Fore.BLACK + text)
    else:
        print(text)
    print(Style.RESET_ALL)


def draw_bbox_multi(img_path, output_path, elem_list, record_mode=False, dark_mode=False):
    imgcv = cv2.imread(img_path)
    count = 1
    for elem in elem_list:
        try:
            top_left = elem.bbox[0]
            bottom_right = elem.bbox[1]
            left, top = top_left[0], top_left[1]
            right, bottom = bottom_right[0], bottom_right[1]
            label = str(count)
            if record_mode:
                if elem.attrib == "clickable":
                    color = (250, 0, 0)
                elif elem.attrib == "focusable":
                    color = (0, 0, 250)
                else:
                    color = (0, 250, 0)
                imgcv = ps.putBText(imgcv, label, text_offset_x=(left + right) // 2 + 10,
                                    text_offset_y=(top + bottom) // 2 + 10,
                                    vspace=10, hspace=10, font_scale=1, thickness=2, background_RGB=color,
                                    text_RGB=(255, 250, 250), alpha=0.5)
            else:
                # text_color = (10, 10, 10) if dark_mode else (255, 250, 250)
                text_color = to_rgb(random.choice(list(CSS4_COLORS.values())))
                text_color = tuple(int(round(c * 255)) for c in text_color)
                bg_color = (128, 128, 128) if dark_mode else (10, 10, 10)
                # imgcv = ps.putBText(imgcv, label, text_offset_x=(left + right) // 2 - 10,
                #                     text_offset_y=(top + bottom) // 2 - 10,
                #                     vspace=10, hspace=10, font_scale=1, thickness=2, background_RGB=bg_color,
                #                     text_RGB=text_color, alpha=0.5)
                imgcv = add_text_with_transparent_bg(imgcv, label, (left, top), text_color=text_color)
                # imgcv = add_text_with_transparent_bg(imgcv, label, ((left + right) // 2 - 10, (top + bottom) // 2 - 10), text_color=text_color)
                imgcv = cv2.rectangle(imgcv, (left, top), (right, bottom), text_color, 2)
        except Exception as e:
            print_with_color(f"ERROR: An exception occurs while labeling the image\n{e}", "red")
        count += 1
    cv2.imwrite(output_path, imgcv)
    return imgcv


def draw_grid(img_path, output_path):
    def get_unit_len(n):
        for i in range(1, n + 1):
            if n % i == 0 and 120 <= i <= 180:
                return i
        return -1

    image = cv2.imread(img_path)
    height, width, _ = image.shape
    color = (255, 116, 113)
    unit_height = get_unit_len(height)
    if unit_height < 0:
        unit_height = 120
    unit_width = get_unit_len(width)
    if unit_width < 0:
        unit_width = 120
    thick = int(unit_width // 50)
    rows = height // unit_height
    cols = width // unit_width
    for i in range(rows):
        for j in range(cols):
            label = i * cols + j + 1
            left = int(j * unit_width)
            top = int(i * unit_height)
            right = int((j + 1) * unit_width)
            bottom = int((i + 1) * unit_height)
            cv2.rectangle(image, (left, top), (right, bottom), color, thick // 2)
            cv2.putText(image, str(label), (left + int(unit_width * 0.05) + 3, top + int(unit_height * 0.3) + 3), 0,
                        int(0.01 * unit_width), (0, 0, 0), thick)
            cv2.putText(image, str(label), (left + int(unit_width * 0.05), top + int(unit_height * 0.3)), 0,
                        int(0.01 * unit_width), color, thick)
    cv2.imwrite(output_path, image)
    return rows, cols


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
