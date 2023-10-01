import numpy
import pytesseract
import cv2
from PIL import Image
import os
import json
import difflib
from .parser import Parser


class Transcripter:
    parser_obj = Parser()

    @classmethod
    def transcript_text_from_image(cls, img: numpy.ndarray, language="eng") -> str:
        """This method transcript text from image, use pytesseract module
        :arg img: numpy array image, language: language in image"""
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.bitwise_not(img)
        img = cv2.resize(img, (300, 50))
        Image.fromarray(img).show()
        total_str = ""
        if language == "eng":
            eng_transcripte = pytesseract.image_to_string(img, lang="eng", config="--psm 6 --oem 3")
            total_str = cls.parser_obj._format_data_for_seach(eng_transcripte)
        else:
            total_str = cls._transcript_not_eng_image(img, language)
        return total_str

    @classmethod
    def _transcript_not_eng_image(cls, img, language: str) -> str:
        """This method transcrip text from image with not english text"""
        addit_data = pytesseract.image_to_data(img, lang=language, output_type=pytesseract.Output.DICT, config="--psm 6 --oem 3")
        eng_data = pytesseract.image_to_data(img, lang="eng", output_type=pytesseract.Output.DICT, config="--psm 6 --oem 3")
        eng_words, eng_conf = cls._convert_data_dict_in_list(eng_data)
        addit_words, addit_conf = cls._convert_data_dict_in_list(addit_data)
        try:
            total_str = ""
            n = 0
            for word in addit_words:
                if addit_conf[n] >= eng_conf[n]:
                    total_str += word
                else:
                    total_str += eng_words[n]
                n += 1
        except Exception as Ex:
            print(Ex)
        finally:
            return cls.parser_obj._format_data_for_seach(total_str)

    @classmethod
    def _convert_data_dict_in_list(cls, in_data_dict: dict):
        """This method delete empty words from dict"""
        words_list = []
        conf_list = []
        n = 0
        for el in in_data_dict['text']:
            if len(el) > 1:
                conf_list.append(in_data_dict['conf'][n])
                words_list.append(in_data_dict['text'][n].lower())
            n += 1
        return words_list, conf_list

    @classmethod
    def find_item_from_json_data(cls, in_str: str, path=f"{os.getcwd()}/items/json_parser/results/items_data.json", language='eng') -> dict:
        with open(path, "r") as file:
            data = json.load(file)

        ratio_dict = {}
        for key, value in data.items():
            matcher = difflib.SequenceMatcher(None, in_str, value[f"{language}Name"])
            if matcher.ratio() >= 0.5:
                ratio_dict[matcher.ratio()] = key
                # print(key, matcher.ratio())
        try:
            # print(max(ratio_dict), "->", ratio_dict[max(ratio_dict)])
            # print(in_str, "->", data[ratio_dict[max(ratio_dict)]]["name"])
            result_dict = data[ratio_dict[max(ratio_dict)]]
        except:
            result_dict = None
        finally:
            return result_dict

    @staticmethod
    def converte_img(path="img.png"):
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        return image


if __name__ == '__main__':
    path = "../crop_dataset"
    list_data = os.listdir(path)
    obj = Transcripter()
    for i in list_data:
        img = obj.converte_img(f"{path}/{i}")
        Image.fromarray(img).show()
        data = obj.transcript_text_from_image(img, "rus")
        print(obj.find_item_from_json_data(in_str=data, language="rus"))
        input("Delay")

