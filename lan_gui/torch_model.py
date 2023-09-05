import torch
import time
import cv2
import mss
import numpy as np
from PIL import Image
import os


class SeachMarkAI:
    def __init__(self, weight_path="./weights.pt", img_width=1920,
                 img_height=1920, delay=0.01, use_delay_flag=False,
                 show_info_flag=False):
        self.img_width = img_width
        self.img_height = img_height
        self.delay = delay
        self.use_delay_flag = use_delay_flag
        self.pre_x_min = 0
        self.pre_x_max = 0
        self.pre_y_min = 0
        self.pre_y_max = 0
        self.run_flag = False           #this flag run or stop while cycle
        self.show_info_flag = show_info_flag
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', weight_path)

    def make_np_screenshot(self) -> np.array:
        """This method make screenshot and convert this in numpy array cv2 module"""
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))
            res = cv2.resize(img, dsize=(self.img_width, self.img_height), interpolation=cv2.INTER_CUBIC)
            return res

    def seach_mark_in_screenshot(self, img: np.array) -> np.array:
        """This method seach object in screenshot and crop if object find"""
        results = self.model(img)
        cord = results.pandas().xyxy[0]
        if self.show_info_flag == True:
            print(f"[INFO] {cord}")
        if cord.empty:          #if object not find in screenshot
            res_img = np.array([])
        else:                   #if object is finded
            x_min = int(cord.xmin[0]) + 5
            x_max = int(cord.xmax[0])
            y_min = int(cord.ymin[0])
            y_max = int(cord.ymax[0])
            if x_min == self.pre_x_min or x_max == self.pre_x_max or y_min == self.pre_y_min or y_max == self.pre_y_max:
                if self.show_info_flag == True:
                    print("Repet screen")
                res_img = np.array([])
            else:
                self.pre_x_min = x_min
                self.pre_x_max = x_max
                self.pre_y_min = y_min
                self.pre_y_max = y_max
                res_img = img[y_min:y_max, x_min:x_max]
        return res_img

    def show_image(self, img) -> None:
        """This is helper method"""
        if img.size != 0:
            Image.fromarray(img).show()

    def run(self) -> None:
        """This method run find object detection in While cycle
        Change self.run_flag to stop cycle"""
        while self.run_flag == True:             #if flag is True -> seach objects in screensonts
            if self.use_delay_flag == True:      #if delay flag is True -> seach objects after delay: default-False
                time.sleep(self.delay)
            img = self.make_np_screenshot()
            crop_img = self.seach_mark_in_screenshot(img)
            self.show_image(crop_img)

    def save_crop_img(self, img: np.array, path: str, img_name: str) -> None:
        if img.size != 0:
            result = Image.fromarray(img)
            result.save(f"{path}/{img_name}.png")


if __name__ == '__main__':
    # time.sleep(5)
    path ="./runs/tarkov_weights/best_s_200.pt"
    obj = SeachMarkAI(weight_path=path, delay=2, use_delay_flag=True, show_info_flag=True)
    obj.run_flag = True
    obj.run()

    # train_path = "./data/images/train"
    # test_path = "./data/images/test"
    # valid_path = "./data/images/valid"
    # train_list = os.listdir("./data/images/train")
    # test_list = os.listdir("./data/images/test")
    # valid_list = os.listdir("./data/images/valid")
    # n = 0
    # for i in train_list:
    #     img = Image.open(train_path + "/" + i)
    #     img = np.array(img)
    #     img = cv2.resize(img, dsize=(obj.img_width, obj.img_height), interpolation=cv2.INTER_CUBIC)
    #     crop_img = obj.seach_mark_in_screenshot(img)
    #     obj.save_crop_img(crop_img, path="./crop_dataset", img_name=f"{n}")
    #     n += 1
    # for i in valid_list:
    #     img = Image.open(valid_path + "/" + i)
    #     img = np.array(img)
    #     img = cv2.resize(img, dsize=(obj.img_width, obj.img_height), interpolation=cv2.INTER_CUBIC)
    #     crop_img = obj.seach_mark_in_screenshot(img)
    #     obj.save_crop_img(crop_img, path="./crop_dataset", img_name=f"{n}")
    #     n += 1
    # for i in test_list:
    #     img = Image.open(test_path + "/" + i)
    #     img = np.array(img)
    #     img = cv2.resize(img, dsize=(obj.img_width, obj.img_height), interpolation=cv2.INTER_CUBIC)
    #     crop_img = obj.seach_mark_in_screenshot(img)
    #     obj.save_crop_img(crop_img, path="./crop_dataset", img_name=f"{n}")
    #     n += 1
