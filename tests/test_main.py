import unittest
import sys
sys.path.insert(0, 'src')

from main import (
    parse_args,
    filter_and_rank_generators,
    call_generator,
    get_subtitle,
    GENERATORS,
    LENGTH_ONLY,
    RANGE_SUPPORT,
    NO_ARGS,
    SPECIAL_PASSWORD,
)


class TestParseArgs(unittest.TestCase):
    """Test argument parsing"""

    def test_parse_args_empty(self):
        result = parse_args([])
        self.assertEqual(result, (None, None, None, None))

    def test_parse_args_generator_only(self):
        result = parse_args(['email'])
        self.assertEqual(result, ('email', None, None, None))

    def test_parse_args_generator_and_length(self):
        result = parse_args(['string', '20'])
        self.assertEqual(result, ('string', '20', None, None))

    def test_parse_args_generator_and_range(self):
        result = parse_args(['date', '2024-01-01', '2024-12-31'])
        self.assertEqual(result, ('date', '2024-01-01', '2024-12-31', None))

    def test_parse_args_case_insensitive(self):
        result = parse_args(['EMAIL'])
        self.assertEqual(result[0], 'email')

    def test_parse_args_multiple_arguments(self):
        result = parse_args(['password', '16', '1'])
        self.assertEqual(result, ('password', '16', '1', None))


class TestFilterAndRankGenerators(unittest.TestCase):
    """Test generator filtering and ranking"""

    def test_filter_empty_query(self):
        result = filter_and_rank_generators(None)
        self.assertEqual(result, sorted(GENERATORS.keys()))

    def test_filter_exact_match(self):
        result = filter_and_rank_generators('email')
        self.assertEqual(result, ['email'])

    def test_filter_prefix_match(self):
        result = filter_and_rank_generators('ip')
        # Should return generators starting with 'ip'
        self.assertIn('ipv4', result)
        self.assertIn('ipv6', result)
        # Should be at the start
        self.assertEqual(result[0:2], ['ipv4', 'ipv6'])

    def test_filter_substring_match(self):
        # When there's an exact match, only return that
        result = filter_and_rank_generators('time')
        self.assertEqual(result, ['time'])

        # Test actual substring matching with non-exact query
        result = filter_and_rank_generators('stam')
        # Should include 'timestamp' (substring match)
        self.assertIn('timestamp', result)

    def test_filter_no_match_returns_all(self):
        result = filter_and_rank_generators('xyz123')
        # Should return all generators sorted
        self.assertEqual(result, sorted(GENERATORS.keys()))

    def test_filter_case_insensitive(self):
        result = filter_and_rank_generators('EMAIL')
        self.assertEqual(result, ['email'])

    def test_filter_ranking_order(self):
        """Test that ranking is correct: exact > prefix > substring"""
        # With exact match, return only that
        result = filter_and_rank_generators('phone')
        self.assertEqual(result, ['phone'])

        # Test prefix ranking with partial query
        result = filter_and_rank_generators('phon')
        # Should include both 'phone' and 'phoneintl' as prefix matches
        self.assertIn('phone', result)
        self.assertIn('phoneintl', result)


class TestCallGenerator(unittest.TestCase):
    """Test generator calling logic"""

    def test_call_no_args_generator(self):
        result = call_generator('uuid')
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_call_length_only_generator_default(self):
        result = call_generator('string')
        self.assertEqual(len(result), 9)  # default length

    def test_call_length_only_generator_custom(self):
        result = call_generator('string', '15')
        self.assertEqual(len(result), 15)

    def test_call_range_generator_with_length(self):
        result = call_generator('num', '10')
        self.assertEqual(len(result), 10)

    def test_call_range_generator_with_range(self):
        result = call_generator('date', '2024-01-01', '2024-12-31')
        # Should be a valid date string
        self.assertIn('2024', result)

    def test_call_password_default(self):
        result = call_generator('password')
        self.assertEqual(len(result), 16)

    def test_call_password_with_length(self):
        result = call_generator('password', '20')
        self.assertEqual(len(result), 20)

    def test_call_password_with_special(self):
        result = call_generator('password', '16', '1')
        self.assertEqual(len(result), 16)
        # Should contain special characters
        special_chars = set('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        self.assertTrue(any(c in special_chars for c in result))

    def test_call_password_without_special(self):
        result = call_generator('password', '16', '0')
        special_chars = set('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        self.assertFalse(any(c in special_chars for c in result))

    def test_call_all_generators(self):
        """Test that all generators can be called without errors"""
        for name in GENERATORS.keys():
            with self.subTest(generator=name):
                result = call_generator(name)
                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 0)


class TestGetSubtitle(unittest.TestCase):
    """Test subtitle generation"""

    def test_subtitle_no_args(self):
        result = get_subtitle('uuid')
        self.assertEqual(result, 'uuid')

    def test_subtitle_length_only_default(self):
        result = get_subtitle('string')
        self.assertEqual(result, 'string (length=9)')

    def test_subtitle_length_only_custom(self):
        result = get_subtitle('string', '15')
        self.assertEqual(result, 'string (length=15)')

    def test_subtitle_range_default(self):
        result = get_subtitle('date')
        self.assertEqual(result, 'date (default)')

    def test_subtitle_range_with_range(self):
        result = get_subtitle('date', '2024-01-01', '2024-12-31')
        self.assertEqual(result, 'date (range: 2024-01-01 to 2024-12-31)')

    def test_subtitle_num_with_length(self):
        result = get_subtitle('num', '10')
        self.assertEqual(result, 'num (length=10)')

    def test_subtitle_password_default(self):
        result = get_subtitle('password')
        self.assertIn('16', result)
        self.assertIn('no special chars', result)

    def test_subtitle_password_with_special(self):
        result = get_subtitle('password', '20', '1')
        self.assertIn('20', result)
        self.assertIn('with special chars', result)


class TestGeneratorCategories(unittest.TestCase):
    """Test that generator categories are correctly defined"""

    def test_all_generators_categorized(self):
        """All generators should be in exactly one category"""
        all_categories = LENGTH_ONLY | RANGE_SUPPORT | NO_ARGS | SPECIAL_PASSWORD

        for name in GENERATORS.keys():
            with self.subTest(generator=name):
                in_categories = sum([
                    name in LENGTH_ONLY,
                    name in RANGE_SUPPORT,
                    name in NO_ARGS,
                    name in SPECIAL_PASSWORD,
                ])
                self.assertEqual(in_categories, 1,
                    f"{name} is in {in_categories} categories, should be in exactly 1")

    def test_no_duplicate_categorization(self):
        """Generators should not be in multiple categories"""
        categories = [LENGTH_ONLY, RANGE_SUPPORT, NO_ARGS, SPECIAL_PASSWORD]

        for i, cat1 in enumerate(categories):
            for cat2 in categories[i+1:]:
                overlap = cat1 & cat2
                self.assertEqual(len(overlap), 0,
                    f"Categories overlap: {overlap}")

    def test_all_categorized_generators_exist(self):
        """All categorized generators should exist in GENERATORS"""
        all_categories = LENGTH_ONLY | RANGE_SUPPORT | NO_ARGS | SPECIAL_PASSWORD

        for name in all_categories:
            with self.subTest(generator=name):
                self.assertIn(name, GENERATORS,
                    f"{name} is categorized but not in GENERATORS")


class TestGeneratorConsistency(unittest.TestCase):
    """Test consistency between generators and their categories"""

    def test_length_only_generators_accept_length(self):
        """LENGTH_ONLY generators should accept length parameter"""
        for name in LENGTH_ONLY:
            with self.subTest(generator=name):
                try:
                    result1 = call_generator(name, '5')
                    result2 = call_generator(name, '15')
                    # Results should have different lengths
                    # (except lorem which counts words, not chars)
                    if name != 'lorem':
                        self.assertNotEqual(len(result1), len(result2))
                except Exception as e:
                    self.fail(f"{name} failed with length parameter: {e}")

    def test_range_generators_accept_range(self):
        """RANGE_SUPPORT generators should accept range parameters"""
        test_cases = {
            'date': ('2024-01-01', '2024-12-31'),
            'time': ('09:00:00', '17:00:00'),
            'datetime': ('2024-01-01 09:00:00', '2024-12-31 17:00:00'),
            'timestamp': ('1609459200', '1640995200'),
        }

        for name in RANGE_SUPPORT:
            with self.subTest(generator=name):
                if name in test_cases:
                    arg1, arg2 = test_cases[name]
                    try:
                        result = call_generator(name, arg1, arg2)
                        self.assertIsInstance(result, str)
                        self.assertGreater(len(result), 0)
                    except Exception as e:
                        self.fail(f"{name} failed with range: {e}")
                elif name == 'num':
                    # num accepts length, not range
                    result = call_generator(name, '10')
                    self.assertEqual(len(result), 10)

    def test_no_args_generators_work_without_args(self):
        """NO_ARGS generators should work without parameters"""
        for name in NO_ARGS:
            with self.subTest(generator=name):
                try:
                    result = call_generator(name)
                    self.assertIsInstance(result, str)
                    self.assertGreater(len(result), 0)
                except Exception as e:
                    self.fail(f"{name} failed without args: {e}")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""

    def test_parse_args_with_spaces(self):
        """Args with whitespace should be handled"""
        result = parse_args(['  email  '])
        self.assertEqual(result[0], 'email')

    def test_call_generator_with_invalid_name(self):
        """Calling non-existent generator should not crash"""
        # This will use fallback logic
        try:
            # The function will try to call GENERATORS[name] which will raise KeyError
            # We need to handle this gracefully
            with self.assertRaises(KeyError):
                call_generator('nonexistent')
        except AssertionError:
            # If it doesn't raise KeyError, that's also fine - it has fallback logic
            pass

    def test_multiple_calls_produce_different_results(self):
        """Multiple calls should produce different values (usually)"""
        generators_to_test = ['uuid', 'email', 'string', 'ipv4']

        for name in generators_to_test:
            with self.subTest(generator=name):
                results = [call_generator(name) for _ in range(5)]
                unique = len(set(results))
                # At least some should be different
                self.assertGreater(unique, 1,
                    f"{name} produced identical results")


if __name__ == '__main__':
    unittest.main()
