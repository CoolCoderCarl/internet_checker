import winsound
import platform
import subprocess
import requests


# duration = 3000
# freq = 500
# winsound.Beep(freq, duration)


urls = ["http://www.google.com", "http://www.yandex.com"]
timeout = 5

for url in urls:
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
