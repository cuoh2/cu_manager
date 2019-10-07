import time

import psutil
from datetime import datetime

import requests

while True:
    url='http://127.0.0.1:8000/manager/save_data/'
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    data={
        "data": psutil.cpu_times().system,
        "time": datetime.now()
    }
    response=requests.post(url=url, data=data, headers=headers)
    print(response.text)
    time.sleep(1)

