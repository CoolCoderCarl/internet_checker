import argparse
import os
import sys
import time
import winsound
from datetime import datetime
from urllib.parse import urlparse

import requests
import validators
from tcp_latency import measure_latency

# Report after run


def get_args():
    """
    Get arguments from CLI
    :return:
    """
    root_parser = argparse.ArgumentParser(
        prog="internet_checker",
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
        help="URL for checking. Example http://www.google.com",
        type=str,
    )
    check_parser.add_argument(
        "-r",
        "--retry",
        dest="retry",
        help="Number of connection attempts to URL",
        type=int,
    )

    return root_parser


# Shortening
namespace = get_args().parse_args(sys.argv[1:])


def timestamp() -> str:
    """
    Get timestamp with hours, minutes & seconds
    Invoke in funcs for get dynamically timestamp
    :return:
    """
    return datetime.now().strftime("%H:%M:%S")


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


def latency_is(url: str, retry_count: int) -> float:
    """
    Return latency value, if request was successfully failed the response will be empty and
    measurement become unavailable then return zero latency
    By default return float
    :param url:
    :param retry_count:
    :return: Return latency in milliseconds, if attempt successfully failed - 0.0
    """
    try:
        return measure_latency(url)[0]
    except IndexError:
        print(
            timestamp()
            + " - Attempt "
            + str(retry_count)
            + ". There is nothing in here at all.",
        )
        return 0.0


def show_response_msg(url: str, retry_count: int):
    """
    Show regular response
    :param url:
    :param retry_count:
    :return:
    """
    response = requests.get("http://" + url, timeout=5)
    if response.status_code == 200:
        print(
            timestamp()
            + " - Attempt "
            + str(retry_count)
            + "| Status Code: "
            + str(response.status_code)
            + ". Latency: "
            + str(latency_is(url, retry_count))
            + " ms."
        )
    else:
        print(
            timestamp()
            + " - Attempt "
            + str(retry_count)
            + " successfully failed. "
            + "| Status Code: "
            + str(response.status_code)
        )
        sound_notification()


def show_exception_msg(retry_count: int):
    """
    Show exception message
    :param retry_count:
    :return:
    """
    print(timestamp() + " - Attempt " + str(retry_count) + " successfully failed.")
    sound_notification(10000, 3000)


def try_internet(url: str, max_retries: int):
    """
    Actually check is internet available
    Make attempts and send messages about statuses
    If catch an exception make a longer noise
    :param url: passed from internet_check() func
    :param max_retries: passed from internet_check() func
    :return:
    """
    retry_count = 0
    if max_retries == 0:
        while True:
            time.sleep(1)
            retry_count += 1
            try:
                show_response_msg(url, retry_count)
            except requests.RequestException:
                show_exception_msg(retry_count)
    else:
        while retry_count < max_retries:
            time.sleep(1)
            retry_count += 1
            try:
                show_response_msg(url, retry_count)
            except requests.RequestException:
                show_exception_msg(retry_count)


def remove_schema(url: str) -> str:
    """
    Remove schema from URL
    :param url:
    :return: Return provided URL without schema
    """
    parsed = urlparse(url)
    scheme = "%s://" % parsed.scheme
    return parsed.geturl().replace(scheme, "", 1)


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
        if parsed_url.scheme == "http":
            try_internet(remove_schema(url), max_retries)
        elif parsed_url.scheme == "https":
            try_internet(remove_schema(url), max_retries)
    else:
        print(url + " is not valid !!!")
        time.sleep(10)
        exit(1)


if __name__ == "__main__":
    if namespace.check == "check":
        internet_check(namespace.url, namespace.retry)
