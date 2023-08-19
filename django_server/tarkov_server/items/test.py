import requests
import json

tmp_dict = {'one': 1, 'two': 2}
log_psw = {'login': 'login', 'password': 'password'}
js = json.dumps(tmp_dict)


url = "http://127.0.0.1:14141/ip/"
login = 'udalo'
password = 'Udalopasha!4'
data = {
    'login': login,
    'password': password
}

responce2 = requests.post(url, data=data)
print(responce2.text)
