import unittest
import re
from datetime import datetime
import sys

sys.path.insert(0, "src")

from generators import (
    random_string,
    random_email,
    random_imei,
    random_unit_number,
    random_uuid,
    random_number,
    random_ipv4,
    random_ipv6,
    random_hex_color,
    random_port,
    random_isbn,
    random_license_plate,
    random_api_key,
    random_base64,
    random_hash,
    random_phone_us,
    random_phone_international,
    random_date,
    random_time,
    random_datetime,
    random_timestamp,
    random_lorem,
    random_username,
    random_password,
)


class TestBasicGenerators(unittest.TestCase):
    """Test basic random generators"""

    def test_random_string_default_length(self):
        result = random_string()
        self.assertEqual(len(result), 10)
        self.assertTrue(result.isalnum())

    def test_random_string_custom_length(self):
        result = random_string(20)
        self.assertEqual(len(result), 20)
        self.assertTrue(result.isalnum())

    def test_random_email_format(self):
        result = random_email()
        self.assertRegex(result, r"^[a-z0-9]+@[a-z0-9]+\.com$")

    def test_random_email_custom_length(self):
        result = random_email(15)
        parts = result.split("@")
        self.assertEqual(len(parts[0]), 15)

    def test_random_number_default_length(self):
        result = random_number()
        self.assertEqual(len(result), 5)
        self.assertTrue(result.isdigit())

    def test_random_number_custom_length(self):
        result = random_number(10)
        self.assertEqual(len(result), 10)
        self.assertTrue(result.isdigit())

    def test_random_uuid_format(self):
        result = random_uuid()
        # UUID4 format: 8-4-4-4-12
        uuid_pattern = r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
        self.assertRegex(result, uuid_pattern)

    def test_random_uuid_uniqueness(self):
        """UUIDs should be unique"""
        results = [random_uuid() for _ in range(100)]
        self.assertEqual(len(results), len(set(results)))


class TestChecksumGenerators(unittest.TestCase):
    """Test generators with checksums"""

    def test_random_imei_length(self):
        result = random_imei()
        self.assertEqual(len(result), 15)
        self.assertTrue(result.isdigit())

    def test_random_imei_custom_length(self):
        result = random_imei(13)
        self.assertEqual(len(result), 14)  # 13 + 1 checksum digit

    def test_random_imei_luhn_checksum(self):
        """Test that IMEI has valid Luhn checksum"""
        imei = random_imei()
        # Luhn algorithm validation
        digits = [int(d) for d in imei]
        checksum = digits[-1]

        tmp = []
        for i, digit in enumerate(digits[:-1]):
            if i % 2:
                digit = digit * 2
            tmp.extend(divmod(digit, 10))

        calculated = (sum(tmp) * 9) % 10
        self.assertEqual(checksum, calculated)

    def test_random_isbn_length(self):
        result = random_isbn()
        self.assertEqual(len(result), 13)
        self.assertTrue(result.startswith("978"))

    def test_random_isbn_checksum(self):
        """Test that ISBN-13 has valid checksum"""
        isbn = random_isbn()
        digits = [int(d) for d in isbn]
        checksum = digits[-1]

        calculated = (
            10 - sum((i % 2 * 2 + 1) * d for i, d in enumerate(digits[:-1])) % 10
        ) % 10
        self.assertEqual(checksum, calculated)

    def test_random_unit_number_format(self):
        result = random_unit_number()
        # Should be: 3 letters + 1 special (UJZ) + digits + checksum
        self.assertGreaterEqual(len(result), 11)  # 4 letters + 6 digits + 1 checksum
        self.assertTrue(result[:3].isupper())
        self.assertIn(result[3], "UJZ")


class TestNetworkGenerators(unittest.TestCase):
    """Test network-related generators"""

    def test_random_ipv4_format(self):
        result = random_ipv4()
        parts = result.split(".")
        self.assertEqual(len(parts), 4)
        for part in parts:
            num = int(part)
            self.assertGreaterEqual(num, 0)
            self.assertLessEqual(num, 255)

    def test_random_ipv6_format(self):
        result = random_ipv6()
        parts = result.split(":")
        self.assertEqual(len(parts), 8)
        for part in parts:
            self.assertLessEqual(len(part), 4)
            int(part, 16)  # Should be valid hex

    def test_random_port_range(self):
        result = random_port()
        port = int(result)
        self.assertGreaterEqual(port, 1024)
        self.assertLessEqual(port, 65535)


class TestWebGenerators(unittest.TestCase):
    """Test web-related generators"""

    def test_random_hex_color_format(self):
        result = random_hex_color()
        self.assertRegex(result, r"^#[A-F0-9]{6}$")

    def test_random_api_key_default_length(self):
        result = random_api_key()
        self.assertEqual(len(result), 32)
        self.assertRegex(result, r"^[a-f0-9]+$")

    def test_random_api_key_custom_length(self):
        result = random_api_key(64)
        self.assertEqual(len(result), 64)

    def test_random_base64_format(self):
        result = random_base64()
        # Base64 should only contain valid characters
        self.assertRegex(result, r"^[A-Za-z0-9+/=]+$")

    def test_random_hash_format(self):
        result = random_hash()
        self.assertEqual(len(result), 64)  # SHA256-like
        self.assertRegex(result, r"^[a-f0-9]{64}$")


class TestIdentityGenerators(unittest.TestCase):
    """Test identity-related generators"""

    def test_random_license_plate_format(self):
        result = random_license_plate()
        self.assertRegex(result, r"^[A-Z]{3}-[0-9]{4}$")

    def test_random_username_default_length(self):
        result = random_username()
        self.assertEqual(len(result), 10)
        self.assertRegex(result, r"^[a-z0-9]+$")

    def test_random_username_custom_length(self):
        result = random_username(15)
        self.assertEqual(len(result), 15)

    def test_random_password_default(self):
        result = random_password()
        self.assertEqual(len(result), 16)
        # Should contain letters and numbers
        self.assertTrue(any(c.isalpha() for c in result))
        self.assertTrue(any(c.isdigit() for c in result))

    def test_random_password_with_special_chars(self):
        result = random_password(20, include_special=True)
        self.assertEqual(len(result), 20)
        # Should contain special characters
        special_chars = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
        self.assertTrue(any(c in special_chars for c in result))

    def test_random_password_without_special_chars(self):
        result = random_password(20, include_special=False)
        special_chars = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
        self.assertFalse(any(c in special_chars for c in result))


class TestCommunicationGenerators(unittest.TestCase):
    """Test communication-related generators"""

    def test_random_phone_us_format(self):
        result = random_phone_us()
        self.assertRegex(result, r"^\(\d{3}\) \d{3}-\d{4}$")

    def test_random_phone_international_format(self):
        result = random_phone_international()
        self.assertRegex(result, r"^\+\d{1,3}-\d{3}-\d{3}-\d{4}$")


class TestDateTimeGenerators(unittest.TestCase):
    """Test date/time generators"""

    def test_random_date_default(self):
        result = random_date()
        # Should be valid ISO date format
        datetime.strptime(result, "%Y-%m-%d")

    def test_random_date_with_range(self):
        result = random_date("2024-01-01", "2024-12-31")
        date = datetime.strptime(result, "%Y-%m-%d")
        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        self.assertGreaterEqual(date, start)
        self.assertLessEqual(date, end)

    def test_random_time_default(self):
        result = random_time()
        self.assertRegex(result, r"^\d{2}:\d{2}:\d{2}$")
        # Should be valid time
        h, m, s = map(int, result.split(":"))
        self.assertLess(h, 24)
        self.assertLess(m, 60)
        self.assertLess(s, 60)

    def test_random_time_with_range(self):
        result = random_time("09:00:00", "17:00:00")
        h, m, s = map(int, result.split(":"))
        self.assertGreaterEqual(h, 9)
        self.assertLessEqual(h, 17)

    def test_random_datetime_default(self):
        result = random_datetime()
        # Should be valid datetime format
        datetime.strptime(result, "%Y-%m-%d %H:%M:%S")

    def test_random_datetime_with_range(self):
        result = random_datetime("2024-01-01 00:00:00", "2024-12-31 23:59:59")
        dt = datetime.strptime(result, "%Y-%m-%d %H:%M:%S")
        start = datetime(2024, 1, 1, 0, 0, 0)
        end = datetime(2024, 12, 31, 23, 59, 59)
        self.assertGreaterEqual(dt, start)
        self.assertLessEqual(dt, end)

    def test_random_timestamp_default(self):
        result = random_timestamp()
        # Should be valid integer timestamp
        timestamp = int(result)
        self.assertGreater(timestamp, 0)

    def test_random_timestamp_with_range(self):
        start_ts = 1609459200  # 2021-01-01
        end_ts = 1640995200  # 2022-01-01
        result = random_timestamp(str(start_ts), str(end_ts))
        timestamp = int(result)
        self.assertGreaterEqual(timestamp, start_ts)
        self.assertLessEqual(timestamp, end_ts)


class TestTextGenerators(unittest.TestCase):
    """Test text generators"""

    def test_random_lorem_default(self):
        result = random_lorem()
        words = result.rstrip(".").split()
        self.assertEqual(len(words), 50)
        # First word should be capitalized
        self.assertTrue(words[0][0].isupper())
        # Should end with period
        self.assertTrue(result.endswith("."))

    def test_random_lorem_custom_length(self):
        result = random_lorem(10)
        words = result.rstrip(".").split()
        self.assertEqual(len(words), 10)

    def test_random_lorem_all_lowercase_except_first(self):
        result = random_lorem(20)
        words = result.rstrip(".").split()
        # First word should start with capital
        self.assertTrue(words[0][0].isupper())
        # Rest should be lowercase
        for word in words[1:]:
            self.assertTrue(word.islower())


class TestGeneratorConsistency(unittest.TestCase):
    """Test that generators produce consistent output types"""

    def test_all_generators_return_strings(self):
        """All generators should return strings"""
        generators = [
            (random_string, ()),
            (random_email, ()),
            (random_imei, ()),
            (random_unit_number, ()),
            (random_uuid, ()),
            (random_number, ()),
            (random_ipv4, ()),
            (random_ipv6, ()),
            (random_hex_color, ()),
            (random_port, ()),
            (random_isbn, ()),
            (random_license_plate, ()),
            (random_api_key, ()),
            (random_base64, ()),
            (random_hash, ()),
            (random_phone_us, ()),
            (random_phone_international, ()),
            (random_date, ()),
            (random_time, ()),
            (random_datetime, ()),
            (random_timestamp, ()),
            (random_lorem, ()),
            (random_username, ()),
            (random_password, ()),
        ]

        for generator, args in generators:
            with self.subTest(generator=generator.__name__):
                result = generator(*args)
                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 0)

    def test_generators_produce_different_values(self):
        """Generators should produce different values on multiple calls"""
        generators = [
            random_string,
            random_email,
            random_number,
            random_ipv4,
            random_uuid,
        ]

        for generator in generators:
            with self.subTest(generator=generator.__name__):
                results = [generator() for _ in range(10)]
                # At least some values should be different
                unique_count = len(set(results))
                self.assertGreater(
                    unique_count, 1, f"{generator.__name__} produced identical values"
                )


if __name__ == "__main__":
    unittest.main()
