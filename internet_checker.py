import os
import sys
import winsound

import requests

# Arg parse for param
# Use URL from args & file
# Use retries from args


def sound_notification(frequency=500, duration=2000):
    if "win" in sys.platform:
        winsound.Beep(frequency, duration)
    else:
        try:
            os.system("beep -f %s -l %s" % (frequency, duration))
        except OSError:
            print("Try to install beep to your system")


def internet_available(url="http://www.google.com"):
    retries = 10
    while retries != 0:
        retries -= 1
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                # exit(0)
                print("Code" + str(response.status_code))

            else:
                sound_notification()
        except requests.RequestException:
            sound_notification()


if __name__ == "__main__":
    internet_available()
