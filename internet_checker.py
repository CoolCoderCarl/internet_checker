import os
import sys
import winsound

import requests

url = "http://www.google.com"
timeout = 5

frequency = 500
duration = 2000


def sound_notification(frequency: int, duration: int):
    if "win" in sys.platform:
        winsound.Beep(frequency, duration)
    else:
        try:
            os.system("beep -f %s -l %s" % (frequency, duration))
        except OSError:
            print("Try to install beep to your system")


def is_internet_available(url: str, timeout: int) -> bool:
    # for url in urls:
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        print(exception)
        return False


if __name__ == "__main__":
    if is_internet_available(url, timeout):
        exit(0)
    else:
        sound_notification(frequency, duration)
