import argparse
import logging
import os
import sys
import time
import winsound
from urllib.parse import urlparse

import requests
import validators
from icmplib import ICMPLibError, ping
from tcp_latency import measure_latency

# Using if args has not been passed
DEFAULT_URL = "https://www.google.com"
DEFAULT_RETRIES = 4

# Using for waiting response after each request
TIMEOUT = 5

# Sound for regular notification
FREQUENCY_NOTIFICATION = 500
DURATION_NOTIFICATION = 1000

# Time sleep
HTTP_SLEEP = 0.25
ICMP_SLEEP = 1


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
        nargs="?",
        const=DEFAULT_URL,
        type=str,
    )
    check_parser.add_argument(
        "-r",
        "--retry",
        dest="retry",
        help="Number of connection attempts to URL",
        nargs="?",
        const=DEFAULT_RETRIES,
        type=int,
    )

    check_parser.add_argument(
        "--icmp",
        dest="icmp",
        action=argparse.BooleanOptionalAction,
        help="Use ICMP protocol",
    )

    check_parser.add_argument(
        "--wifi",
        dest="wifi",
        help="WiFi Interface name",
        type=str,
    )

    return root_parser


# Shortening
namespace = get_args().parse_args(sys.argv[1:])

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.CRITICAL
)


def sound_notification(
    frequency=FREQUENCY_NOTIFICATION, duration=DURATION_NOTIFICATION
):
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
        except OSError as os_err:
            logging.error(f"Error: {os_err}")
            logging.critical("Try to install beep to your system")


def restart_interface(ifname: str):
    """
    Restart interface
    :param ifname:
    :return:
    """
    # TODO wired interface
    if namespace.wifi:
        logging.info(f"Going to reconnect WiFi interface {ifname}...")
        os.system("netsh wlan disconnect")
        time.sleep(5)
        os.system(f"netsh wlan connect {ifname}")


def latency_is(url: str, retry_count: int) -> float:
    """
    Return latency value, if request was successfully failed the response will be empty and
    measurement become unavailable then return zero latency
    :param url:
    :param retry_count:
    :return: Return latency in milliseconds, if attempt successfully failed - 0.0
    """
    try:
        return measure_latency(url)[0]
    except IndexError as index_err:
        logging.error(
            f"Attempt {retry_count}. There is nothing in here at all. Error: {index_err}"
        )
        return 0.0


def http_requests(url: str, retry_count: int):
    """
    Show messages after requests using HTTP
    :param url:
    :param retry_count:
    :return:
    """
    try:
        response = requests.get("http://" + url, timeout=TIMEOUT)
        if response.status_code == 200:
            logging.info(
                f"Attempt {retry_count} | Status code: {response.status_code} - Latency: {latency_is(url, retry_count)} ms."
            )
        else:
            logging.warning(
                f"Attempt {retry_count} successfully failed. | Status code: {response.status_code}"
            )
            sound_notification()
    except requests.RequestException as request_err:
        logging.error(f"Error: {request_err}")
        show_exception_msg(retry_count)
        restart_interface(namespace.wifi)


def icmp_requests(url: str, retry_count: int):
    """
    Show messages after requests using ICMP
    :param url:
    :param retry_count: Need to use, because report returned after each request
    :return:
    """
    try:
        host = ping(url, count=1, timeout=TIMEOUT)
        if host.is_alive:
            logging.info(
                f"Attempt {retry_count} | Is host available: {host.is_alive} - Average RTT: {host.avg_rtt}"
            )
        else:
            logging.warning(
                f"Attempt {retry_count} successfully failed. | Is host available: {host.is_alive}"
            )
            sound_notification()
    except ICMPLibError as icmp_err:
        logging.error(f"Error: {icmp_err}")
        show_exception_msg(retry_count)
        restart_interface(namespace.wifi)


def show_exception_msg(retry_count: int):
    """
    Show exception message
    :param retry_count:
    :return:
    """
    logging.critical(f"Attempt {retry_count} successfully failed.")
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
            retry_count += 1
            try:
                if namespace.icmp:
                    time.sleep(ICMP_SLEEP)
                    icmp_requests(url, retry_count)
                else:
                    time.sleep(HTTP_SLEEP)
                    http_requests(url, retry_count)
            except requests.RequestException as request_err:
                logging.error(f"Error: {request_err}")
                show_exception_msg(retry_count)
    else:
        while retry_count < max_retries:
            retry_count += 1
            try:
                if namespace.icmp:
                    time.sleep(ICMP_SLEEP)
                    icmp_requests(url, retry_count)
                else:
                    time.sleep(HTTP_SLEEP)
                    http_requests(url, retry_count)
            except requests.RequestException as request_err:
                logging.error(f"Error: {request_err}")
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
        logging.critical(f"{url} is not valid !!!")
        time.sleep(5)
        exit(1)


if __name__ == "__main__":
    if namespace.check == "check":
        internet_check(namespace.url, namespace.retry)
