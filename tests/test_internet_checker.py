from internet_checker import internet_checker as i_c

DEFAULT_URL = "http://www.google.com"


def test_latency_is():
    return isinstance(i_c.latency_is(DEFAULT_URL, 1), float)


if __name__ == "__main__":
    pass
