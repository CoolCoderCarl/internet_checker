import argparse
import os
import sys
import winsound

import requests

# Use URL from args & file


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

    return root_parser


# Shortening
namespace = get_args().parse_args(sys.argv[1:])


def sound_notification(frequency=500, duration=2000):
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


def internet_available(url: str, max_retries: int):
    # RegExp URL
    num_retry = 0
    while num_retry < max_retries:
        num_retry += 1
        try:
            response = requests.get("https://" + url, timeout=5)
            if response.status_code == 200:
                print(
                    "Attempt "
                    + str(num_retry)
                    + ". Return Status Code: "
                    + str(response.status_code)
                )

            else:
                sound_notification()
        except requests.RequestException:
            sound_notification()


if __name__ == "__main__":
    if namespace.check == "check":
        internet_available(namespace.url, namespace.retry)
