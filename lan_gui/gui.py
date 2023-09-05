import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt
import requests
import cv2
import mss
import numpy as np
import time
import keyboard
import json_numpy
from PIL import Image


class TarkovSellGui(QtWidgets.QMainWindow):
    LANGUAGES = ("rus", "eng")

    def __init__(self, img_width=1280, img_height=1280, delay=0.1,):
        super().__init__()
        self.ui = uic.loadUi('sell.ui')
        self._init_widgets()
        self.img_width = img_width
        self.img_height = img_height
        self.delay = delay
        self.setFocus()
        self.ui.button.clicked.connect(lambda: self._test_connect())
        self.key = keyboard
        self.key.on_press_key("z", lambda _:self.get_item_data())

    def _init_widgets(self):
        self.ui.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.ui.setWindowTitle("Sell")
        self.ui.box_lng.addItems(self.LANGUAGES)
        self.ui.button.setText('test')
        self.ui.button.setStyleSheet('QPushButton {background-color: green;}')
        self.ui.one_slot_price.setText("-")
        self.ui.trader_slot.setText("-")
        self.ui.trader_price_slot.setText("-")


    def _test_connect(self):
        """This method start or stop seaching image in monitor"""
        url = "http://localhost:8000/test/"
        data = {
            'login': self.ui.login_edit.text(),
            'password': self.ui.password_edit.text()
        }
        responce = requests.post(url=url, data=data)
        res_data = responce.json()
        self.ui.one_slot_price.setText(res_data['status'])
        self.ui.trader_slot.setText(res_data['status'])
        self.ui.trader_price_slot.setText(res_data['status'])


    def make_np_screenshot(self) -> np.array:
        """This method make screenshot and convert this in numpy array cv2 module"""
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))
            res = cv2.resize(img, dsize=(self.img_width, self.img_height), interpolation=cv2.INTER_CUBIC)
            res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
            return res

    def get_item_data(self) -> None:
        url = "http://localhost:8000/item/"
        lng = self.ui.box_lng.currentText()
        img = self.make_np_screenshot()
        json_np = json_numpy.dumps(img)
        login = self.ui.login_edit.text()
        password = self.ui.password_edit.text()
        data = {
            'json': json_np,
            'login': login,
            'password': password,
            'lng': lng
        }
        response = requests.post(url=url, data=data)
        if response.status_code == 200:
            res_dict = response.json()
            self._insert_prices(res_dict)

    def show_image(self, img) -> None:
        """This is helper method"""
        if img.size != 0:
            Image.fromarray(img).show()


    def _insert_prices(self, price_dict):
        """This method show item data in GUI"""
        print(price_dict['traderName'])
        print(price_dict['traderPrice'])
        print(price_dict['pricePerSlot'])
        if price_dict['canSellOnFlea'] == True:
            self.ui.one_slot_price.setText(str(price_dict["pricePerSlot"]))
        else:
            self.ui.one_slot_price.setText(str('Ban'))
        self.ui.trader_slot.setText(price_dict['traderName'])
        self.ui.trader_price_slot.setText(str(price_dict['traderPrice']))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    open = TarkovSellGui()
    open.ui.show()
    sys.exit(app.exec_())
