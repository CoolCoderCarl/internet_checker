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


def is_internet_available(url: str):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            sys.exit(0)
        else:
            sound_notification(frequency, duration)
    except (
        requests.ConnectionError,
        requests.Timeout
    ):
        sound_notification(frequency, duration)


if __name__ == "__main__":
    is_internet_available(url)
