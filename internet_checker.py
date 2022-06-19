import argparse
import os
import sys
import time
import winsound
from urllib.parse import urlparse

import requests
import validators


def get_args():
    """
    Get arguments from CLI
    :return:
    """
    root_parser = argparse.ArgumentParser(
        prog="butler",
        description="""Check the Internet connection""",
        epilog="""(c) CoolCoderCarl""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    internet_check_parser = root_parser.add_subparsers(dest="check")

    check_parser = internet_check_parser.add_parser(
        "check",
        help="Check Internet connection trying to connect to provided URL",
    )
    check_parser.add_argument(
        "--url",
        dest="url",
        help="URL for checking",
        type=str,
    )
    check_parser.add_argument(
        "-r",
        "--retry",
        dest="retry",
        help="How much try to connect to URL",
        type=int,
    )

    # From file
    # Path to file
    # Retries

    return root_parser


# Shortening
namespace = get_args().parse_args(sys.argv[1:])


def sound_notification(frequency=500, duration=1000):
    """
    Play system sound with beep
    If Linux maybe require to install beep package
    :param frequency:
    :param duration:
    :return:
    """
    if "win" in sys.platform:
        winsound.Beep(frequency, duration)
    else:
        try:
            os.system("beep -f %s -l %s" % (frequency, duration))
        except OSError:
            print("Try to install beep to your system")


def try_checking(url: str, max_retries: int):
    """
    Actually check is internet available
    While it is available send a message about status code
    Make attempts and send messages about statuses
    If catch an exception make a longer noise
    :param url: passed from internet_check() func
    :param max_retries: passed from internet_check() func
    :return:
    """
    num_retry = 0
    while num_retry < max_retries:
        time.sleep(1)
        num_retry += 1
        try:
            response = requests.get("http://" + url, timeout=5)
            if response.status_code == 200:
                print(
                    "Attempt "
                    + str(num_retry)
                    + ". Return Status Code: "
                    + str(response.status_code)
                )

            else:
                print("Attempt " + str(num_retry) + " failed")
                sound_notification()
        except requests.RequestException:
            sound_notification(10000, 3000)


def internet_check(url: str, max_retries: int):
    """
    Check if Internet available, if not make sound
    https is not available and will change automatically to http
    :param url: passed to try_checking() func
    :param max_retries: passed to try_checking() func
    :return:
    """
    if validators.url(url):
        parsed_url = urlparse(url)
        if parsed_url.scheme == "https":
            try_checking(url, max_retries)
        elif parsed_url.scheme == "http":
            try_checking(url, max_retries)
        elif parsed_url.scheme == "":
            try_checking(url, max_retries)
    else:
        print(url + " not valid !!!")
        print("Your attempt successfully failed.")
        time.sleep(10)
        exit(1)


if __name__ == "__main__":
    if namespace.check == "check":
        internet_check(namespace.url, namespace.retry)
