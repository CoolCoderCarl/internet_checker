import os
import sys
import winsound

import requests

# Arg parse for param
# Use URL from args & file
url = "https://www.google.com"

frequency = 500
duration = 2000


# def sound_notification(frequency: int, duration: int):


def internet_available(url: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            sys.exit(0)
    except (requests.ConnectionError, requests.Timeout):
        if "win" in sys.platform:
            winsound.Beep(frequency, duration)
        else:
            try:
                os.system("beep -f %s -l %s" % (frequency, duration))
            except OSError:
                print("Try to install beep to your system")


if __name__ == "__main__":
    internet_available(url)
