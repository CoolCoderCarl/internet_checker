import os
import sys
import time
import winsound

import requests

# Arg parse for param
# Use URL from args & file
url = "https://www.google.com"

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


def is_internet_available(url: str) -> bool:
    # for url in urls:
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
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
    if is_internet_available(url):
        print("Connected to the Internet")
        # sys.exit(0)
    else:
        print("No Internet connection")
        sound_notification(frequency, duration)

    time.sleep(10)
