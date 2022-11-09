from internet_checker import internet_checker as i_c

DEFAULT_URL = "https://www.google.com"


def test_latency_is(url: str, retry_count: int):
    isinstance(i_c.latency_is(url, retry_count), float)


if __name__ == "__main__":
    pass
