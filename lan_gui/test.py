import requests


url = "http://localhost:8000/test/"
one = {'one': 1}
two = {'two': 2}

unite = {'one': one, "two": two}


response = requests.post(url=url, data=unite)
