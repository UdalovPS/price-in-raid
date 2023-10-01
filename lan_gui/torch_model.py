import numpy as np
from PIL import Image
from ultralytics import YOLO


class SeachMarkAI:
    def __init__(self, weight_path="./yolov8_weights.pt", show_info_flag=False):
        self.pre_x_min = 0
        self.pre_x_max = 0
        self.pre_y_min = 0
        self.pre_y_max = 0
        self.img_width = 1280
        self.img_height = 1280
        self.show_info_flag = show_info_flag
        # self.model = torch.hub.load('./items/ai_model/yolov5', 'custom', path=weight_path, source='local')
        self.model = YOLO(weight_path)

    def seach_mark_in_screenshot(self, img: np.array) -> np.array:
        """This method seach object in screenshot and crop image if object find"""
        try:
            result = self.model.predict(img)
            box = result[0].boxes[0]
            cords = box.xyxy[0].tolist()
            if self.show_info_flag == True:
                print(f"[INFO] {cords}")
            x_min = int(cords[0]) + 3
            x_max = int(cords[2])
            y_min = int(cords[1])
            y_max = int(cords[3])
            res_img = img[y_min:y_max, x_min:x_max]
            return res_img
        except:
            if self.show_info_flag == True:
                print(f"[INFO] object not find")
            return np.array([])


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
    model_path ="./yolov8_weights.pt"
    obj = SeachMarkAI(weight_path=model_path, show_info_flag=True)
    image_path = "./129.png"
    img = obj.open_test_image(image_path)
    crop_img = obj.seach_mark_in_screenshot(img)
    obj.show_image(crop_img)
