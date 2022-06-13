import os
import sys
import time
import winsound

import requests

# Arg parse for param ?
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
    try:
        request = requests.get(url, timeout=timeout)
        if request.status_code == 200:
            return True
        else:
            return False
    except (
        requests.ConnectionError,
        requests.Timeout,
        requests.HTTPError,
        requests.TooManyRedirects,
    ) as exception:
        print(exception)
        return False


if __name__ == "__main__":
    if is_internet_available(url, timeout):
        print("Connected to the Internet")
    else:
        print("No Internet connection")
        sound_notification(frequency, duration)

    time.sleep(10)
