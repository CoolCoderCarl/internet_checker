import os
import sys
import winsound

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# Arg parse for param
# Use URL from args & file
url = "https://www.google.com"
timeout = 5

frequency = 500
duration = 2000


def sound_notification(frequency: int, duration: int):
    if "win" in sys.platform.lower():
        winsound.Beep(frequency, duration)
    else:
        try:
            os.system("beep -f %s -l %s" % (frequency, duration))
        except OSError:
            print("Try to install beep to your system")


def is_internet_available(url: str, timeout: int) -> bool:
    # for url in urls:
    retry_strategy = Retry(total=100, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("http://", adapter)
    http.mount("https://", adapter)
    try:
        response = http.get(url, timeout=timeout)
        if response.status_code == 200:
            print("Connected to the Internet")
            return True
        else:
            return False
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No Internet connection")
        print(exception)
        return False


if __name__ == "__main__":
    if is_internet_available(url, timeout):
        exit(0)
    else:
        sound_notification(frequency, duration)
