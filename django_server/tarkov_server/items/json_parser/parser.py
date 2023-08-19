from concurrent.futures import ThreadPoolExecutor
import progressbar

import itertools
import requests
import datetime

import base64
import json
import urllib.parse

import os


class Parser:
    # Количество потоков
    NUM_THREADS = 8

    # Таймаут запроса
    TIMEOUT = 5

    # Размер страницы, при больших значениях сайт так же даёт 20
    PAGE_SIZE = 20

    # Количество страниц на ThreadPoolExecutor
    SECTION_SIZE = 200

    # Папка с результатами
    RESULT_DIR = "./results"

    CHANGE_DICT = {
            "а":"a", "б":"6", "в":"8", "г":"r", "д":"d", "е":"e", "з":"3", "й":"u", "и":"u", "к":"k", "м":"m", "н":"h", "о":"0", "п":"n", "р":"p", "с":"c", "т":"t", "у":"y","щ":"ш", "э":"9", "х":"x",
            "g":"9", "i":"1", "s":"5", "o":"0", "l":'1',
            "|":'', "/":"", ".":"", "'":"", "-":"", '"':"", "@":"0", "`":"", "!":"1", " ":"", "(":"", ")":"",
    }

    COOKIES = {
        "HCLBSTICKY": "7f76f66e77d2b3ac641033a0dc08487a|Y7SgC|Y7SgB",
    }

    HEADERS = {
        "authority": "tarkov-market.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://tarkov-market.com/",
        "sec-ch-ua": '"Chromium";v="106", "Yandex";v="22", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0",
    }

    @classmethod
    def start(cls):
        itemLinks = cls._parseAllItemLinks()

        # Удостовериться, что папка с резльтатами существует
        os.makedirs(cls.RESULT_DIR, exist_ok=True)

        # filename = datetime.datetime.now().strftime("%d.%m.%y %H_%M") + ".json"
        filename = "items_data.json"

        json.dump(
            itemLinks,
            open(f"{cls.RESULT_DIR}/{filename}", "w", encoding="utf-8")
        )

    @classmethod
    def _parseAllItemLinks(cls):
        allItemLinks = {}

        # Так как сайт не даёт информации об общем количестве страниц, парсим по {SECTION_SIZE} за раз и проверяем, закончились ли товары
        for sectionIndex in itertools.count():
            startPage, endPage = sectionIndex*cls.SECTION_SIZE, (sectionIndex+1)*cls.SECTION_SIZE
            print(f"Pages {startPage+1}-{endPage}")

            # Параллельные запросы
            executor = ThreadPoolExecutor(max_workers=cls.NUM_THREADS)
            iterator = executor.map(
                cls._parsePageItems,
                range(startPage, endPage)
            )

            for pageItems in progressbar.progressbar(iterator, max_value=cls.SECTION_SIZE):
                if len(pageItems) == 0:
                    # Если на странице 0 результатов - завершаем цикл
                    # Выполнятся ещё максимум {NUM_THREADS - 1} заданий, находящихся в очереди, то есть отправятся запросы на пустые страницы со слишком большим номером
                    executor.shutdown(wait=False)
                    break

                # Добавляем ссылки из товаров со страницы в общий массив
                for item in pageItems:
                    try:
                        tmp_dict = {}
                        tmp_dict["name"] = item["shortName"]
                        tmp_dict['engName'] = cls._format_data_for_seach(item['name'])
                        tmp_dict['rusName'] = cls._format_data_for_seach(item['ruName'])
                        tmp_dict['pricePerSlot'] = item['pricePerSlot']
                        tmp_dict['traderName'] = item['traderName']
                        tmp_dict['traderPrice'] = item['traderPrice']
                        tmp_dict["canSellOnFlea"] = item["canSellOnFlea"]
                        allItemLinks[item['shortName']] = tmp_dict
                    except:
                        continue
                    # allItemLinks.append(
                    #     f"https://tarkov-market.com/item/{item['url']}"
                    # )

            if len(pageItems) == 0: break

        return allItemLinks

    @classmethod
    def _format_data_for_seach(cls, in_string: str) -> str:
        """This method formate string for seach in AI string
        Use CHANGE_DICT
        """
        result_str = ""
        for letter in in_string.lower():
            if letter in cls.CHANGE_DICT:
                result_str += cls.CHANGE_DICT[letter]
            else:
                result_str += letter
        # print("RES STR: ", result_str)
        return result_str

    @classmethod
    def _parsePageItems(cls, pageNumber=0):
        """Функция парсинга товаров со страницы {pageNumber}"""

        params = {
            "lang": "en",
            "search": "",
            "tag": "",
            "sort": "change24",
            "sort_direction": "desc",
            "trader": "",
            "skip": pageNumber * cls.PAGE_SIZE,
            "limit": cls.PAGE_SIZE,
        }

        # Сервер может перестать отвечать на слишком быстрые запросы, потому ждём таймаут и в случае его отправляем ещё раз
        while True:
            try:
                response = requests.get("https://tarkov-market.com/api/items",
                    params=params,
                    headers=cls.HEADERS,
                    cookies=cls.COOKIES,
                    timeout=cls.TIMEOUT
                ).json()

                break
            
            except requests.exceptions.Timeout:
                pass

        return cls._decodeItems(response["items"])
        
    @staticmethod
    def _decodeItems(encodedItems):
        """Расшфровка товаров"""

        # Которая содержит товары в json
        return json.loads(
            # Которая содержит url-encoded строку
            urllib.parse.unquote(
                # Далее это просто base64 строка
                base64.b64decode(
                    # Вся хитрость была в этом, надо просто убрать с 6 по 10 символы из исходной строки
                    encodedItems[:5] + encodedItems[10:]
                ).decode("utf-8")
            )
        )


if __name__ == "__main__":
    p = Parser()
    p.start()
