import winsound

import requests

# duration = 3000
# freq = 500
# winsound.Beep(freq, duration)


def is_internet_available():
    urls = "http://www.google.com"
    timeout = 5

    # for url in urls:
    try:
        request = requests.get(urls, timeout=timeout)
        print("Connected to the Internet")
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        print(exception)
        return False


print(is_internet_available())
