import torch
import cv2
import numpy as np
from PIL import Image


class SeachMarkAI:
    def __init__(self, weight_path="./weights.pt", show_info_flag=False):
        self.pre_x_min = 0
        self.pre_x_max = 0
        self.pre_y_min = 0
        self.pre_y_max = 0
        self.img_width = 1920
        self.img_height = 1920
        self.show_info_flag = show_info_flag
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', weight_path)

    def seach_mark_in_screenshot(self, img: np.array) -> np.array:
        """This method seach object in screenshot and crop image if object find"""
        results = self.model(img)
        cord = results.pandas().xyxy[0]
        if self.show_info_flag == True:
            print(f"[INFO] {cord}")
        if cord.empty:          #if object not find in screenshot
            res_img = np.array([])
        else:                   #if object is finded
            x_min = int(cord.xmin[0]) + 3
            x_max = int(cord.xmax[0])
            y_min = int(cord.ymin[0])
            y_max = int(cord.ymax[0])
            res_img = img[y_min:y_max, x_min:x_max]
        return res_img

    def show_image(self, img) -> None:
        """This is helper method need for show result image"""
        if img.size != 0:
            Image.fromarray(img).show()

    def save_crop_img(self, img: np.array, path: str, img_name: str) -> None:
        if img.size != 0:
            result = Image.fromarray(img)
            result.save(f"{path}/{img_name}.png")

    def open_test_image(self, img_path: str) -> np.array:
        """This method open test image, convetr to numpy and resize for need size"""
        img = Image.open(img_path)
        res = np.array(img.resize((self.img_width, self.img_height)))
        return res

if __name__ == '__main__':
    model_path ="./model_weight.pt"
    obj = SeachMarkAI(weight_path=model_path, show_info_flag=True)
    image_path = "./129.png"
    img = obj.open_test_image(image_path)
    crop_img = obj.seach_mark_in_screenshot(img)
    obj.show_image(crop_img)
