import json

import requests
import json_numpy
import numpy as np
from PIL import Image

url = "http://127.0.0.1:8000/item/"
image_path = "./129.png"
login = 'admin'
password = 'admin_password'
lng = 'rus'

img = Image.open(image_path)
# img_numpy = np.array(img.resize((1920, 1920)))
img_numpy = np.array(img)
json_np = json_numpy.dumps(img_numpy)

data = {
    'json': json_np,
    'login': login,
    'password': password,
    'lng': lng
}
response = requests.post(url=url, data=data)
if response.status_code == 200:
    item_data = json.loads(response.content)
    print(item_data)
