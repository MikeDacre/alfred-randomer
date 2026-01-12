from uuid import uuid4
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import choice, randint, uniform
from datetime import datetime, timedelta
from base64 import b64encode
import time

LETTER_VALUES = dict(zip(ascii_uppercase, filter(lambda i: i % 11, range(10, 39))))


def random_string(length=10):
    return "".join(choice(ascii_lowercase + ascii_uppercase) for _ in range(length))


def random_email(length=10):
    return "".join([random_string(length), "@", random_string(7), ".com"]).lower()


def random_imei(length=14):
    imei = [randint(0, 9) for _ in range(length)]

    tmp = []

    for index, digit in enumerate(imei):
        if index % 2:
            digit = digit * 2

        tmp.extend(divmod(digit, 10))

    imei.append((sum(tmp) * 9) % 10)
    return "".join(map(str, imei))


def random_number(length=5):
    return "".join(str(randint(0, 9)) for _ in range(length))


def random_unit_number(length=6):
    unit_number = [
        choice(ascii_uppercase),
        choice(ascii_uppercase),
        choice(ascii_uppercase),
        choice("UJZ")
    ]
    # Add the numeric digits
    unit_number.extend([randint(0, 9) for _ in range(length)])

    values = list(map(lambda d: int(LETTER_VALUES.get(d, d)), unit_number))
    checksum = sum(d * 2**i for i, d in enumerate(values)) % 11

    if checksum > 9:
        return random_unit_number(length=length)

    unit_number.append(checksum)
    return "".join(map(str, unit_number))


def random_uuid():
    return str(uuid4())


def random_ipv4():
    return ".".join(str(randint(0, 255)) for _ in range(4))


def random_ipv6():
    return ":".join(f"{randint(0, 65535):04x}" for _ in range(8))


def random_hex_color():
    return f"#{randint(0, 0xFFFFFF):06X}"


def random_port():
    return str(randint(1024, 65535))


def random_isbn():
    # Generate ISBN-13 with valid checksum
    isbn = [9, 7, 8] + [randint(0, 9) for _ in range(9)]
    checksum = (10 - sum((i % 2 * 2 + 1) * d for i, d in enumerate(isbn)) % 10) % 10
    isbn.append(checksum)
    return "".join(map(str, isbn))


def random_license_plate():
    # US format: ABC-1234
    letters = "".join(choice(ascii_uppercase) for _ in range(3))
    numbers = "".join(str(randint(0, 9)) for _ in range(4))
    return f"{letters}-{numbers}"


def random_api_key(length=32):
    return "".join(choice("0123456789abcdef") for _ in range(length))


def random_base64(length=16):
    random_bytes = bytes(randint(0, 255) for _ in range(length))
    return b64encode(random_bytes).decode('ascii')


def random_hash():
    # SHA256-like hash (64 hex characters)
    return "".join(choice("0123456789abcdef") for _ in range(64))


def random_phone_us():
    area = randint(200, 999)
    exchange = randint(200, 999)
    subscriber = randint(0, 9999)
    return f"({area}) {exchange}-{subscriber:04d}"


def random_phone_international():
    country = randint(1, 999)
    area = randint(100, 999)
    exchange = randint(100, 999)
    subscriber = randint(1000, 9999)
    return f"+{country}-{area}-{exchange}-{subscriber}"


def random_date(start=None, end=None):
    if start and end:
        # Parse date strings and generate random date in range
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        delta = end_date - start_date
        random_days = randint(0, delta.days)
        random_date = start_date + timedelta(days=random_days)
        return random_date.strftime("%Y-%m-%d")
    else:
        # Generate random date in last/next year
        today = datetime.now()
        start_date = today - timedelta(days=365)
        end_date = today + timedelta(days=365)
        delta = end_date - start_date
        random_days = randint(0, delta.days)
        random_date = start_date + timedelta(days=random_days)
        return random_date.strftime("%Y-%m-%d")


def random_time(start=None, end=None):
    if start and end:
        # Parse time strings HH:MM:SS and generate random time in range
        start_parts = list(map(int, start.split(":")))
        end_parts = list(map(int, end.split(":")))
        start_seconds = start_parts[0] * 3600 + start_parts[1] * 60 + start_parts[2]
        end_seconds = end_parts[0] * 3600 + end_parts[1] * 60 + end_parts[2]
        random_seconds = randint(start_seconds, end_seconds)
    else:
        # Generate random time in 24h range
        random_seconds = randint(0, 86399)

    hours = random_seconds // 3600
    minutes = (random_seconds % 3600) // 60
    seconds = random_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def random_datetime(start=None, end=None):
    if start and end:
        # Parse datetime strings and generate random datetime in range
        start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        delta = end_dt - start_dt
        random_seconds = randint(0, int(delta.total_seconds()))
        random_dt = start_dt + timedelta(seconds=random_seconds)
        return random_dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        # Generate random datetime in last/next year
        date_part = random_date()
        time_part = random_time()
        return f"{date_part} {time_part}"


def random_timestamp(start=None, end=None):
    if start and end:
        # Interpret as timestamp range
        start_ts = int(start)
        end_ts = int(end)
        return str(randint(start_ts, end_ts))
    else:
        # Generate timestamp in last/next year range
        now = int(time.time())
        year_seconds = 365 * 24 * 3600
        return str(randint(now - year_seconds, now + year_seconds))


def random_lorem(length=50):
    """Generate lorem ipsum text with 'length' words"""
    lorem_words = [
        "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing",
        "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore",
        "et", "dolore", "magna", "aliqua", "enim", "ad", "minim", "veniam",
        "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "aliquip",
        "ex", "ea", "commodo", "consequat", "duis", "aute", "irure", "in",
        "reprehenderit", "voluptate", "velit", "esse", "cillum", "fugiat",
        "nulla", "pariatur", "excepteur", "sint", "occaecat", "cupidatat",
        "non", "proident", "sunt", "culpa", "qui", "officia", "deserunt",
        "mollit", "anim", "id", "est", "laborum"
    ]
    selected_words = [choice(lorem_words) for _ in range(length)]
    # Capitalize first word
    if selected_words:
        selected_words[0] = selected_words[0].capitalize()
    return " ".join(selected_words) + "."


def random_username(length=10):
    return "".join(choice(ascii_lowercase + digits) for _ in range(length))


def random_password(length=16, include_special=False):
    chars = ascii_lowercase + ascii_uppercase + digits
    if include_special:
        chars += punctuation
    return "".join(choice(chars) for _ in range(length))
