import os
import sys
import time
import winsound

import requests

# Arg parse for param
# Use URL from args & file


def sound_notification(frequency=500, duration=2000):
    if "win" in sys.platform:
        winsound.Beep(frequency, duration)
    else:
        try:
            os.system("beep -f %s -l %s" % (frequency, duration))
        except OSError:
            print("Try to install beep to your system")


def internet_available(url="http://www.google.com"):
    try:
        response = requests.get(url, timeout=5)
        print(response.status_code)
        if response.status_code == 200:
            exit(0)
        else:
            sound_notification()
    except (requests.ConnectionError, requests.Timeout) as err:
        print(err)
        # sound_notification()


if __name__ == "__main__":
    internet_available()
    time.sleep(10)
