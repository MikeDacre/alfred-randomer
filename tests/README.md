# Tests

Comprehensive test suite for the Alfred Randomer workflow.

## Running Tests

```bash
# Run all tests
make test

# Run with verbose output
make test-verbose

# Generate coverage report
make test-coverage
```

## Test Files

### test_generators.py

Tests all 24 random value generators with 100% code coverage:

**TestBasicGenerators** - Core generators
- `random_string` - Length validation, alphanumeric check
- `random_email` - Format validation (user@domain.com)
- `random_number` - Length and digit validation
- `random_uuid` - UUID4 format and uniqueness

**TestChecksumGenerators** - Generators with validation algorithms
- `random_imei` - Luhn algorithm checksum validation
- `random_isbn` - ISBN-13 checksum validation
- `random_unit_number` - ISO 6346 container number format

**TestNetworkGenerators** - Network-related values
- `random_ipv4` - Valid IPv4 address (0-255 range)
- `random_ipv6` - Valid IPv6 format
- `random_port` - Port range (1024-65535)

**TestWebGenerators** - Web development values
- `random_hex_color` - Hex color format (#RRGGBB)
- `random_api_key` - Hex string validation
- `random_base64` - Base64 encoding validation
- `random_hash` - SHA256-like hash format

**TestIdentityGenerators** - Identity values
- `random_license_plate` - US format (ABC-1234)
- `random_username` - Lowercase alphanumeric
- `random_password` - With/without special characters

**TestCommunicationGenerators** - Contact information
- `random_phone_us` - US format (555) 123-4567
- `random_phone_international` - International format +1-555-123-4567

**TestDateTimeGenerators** - Date/time with range support
- `random_date` - ISO date format, range validation
- `random_time` - HH:MM:SS format, range validation
- `random_datetime` - Combined datetime, range validation
- `random_timestamp` - Unix timestamp, range validation

**TestTextGenerators** - Text generation
- `random_lorem` - Lorem ipsum word count, capitalization

**TestGeneratorConsistency** - Cross-cutting concerns
- All generators return strings
- All generators produce different values
- Format consistency

### test_main.py

Tests workflow logic and argument handling with 80% coverage:

**TestParseArgs** - Argument parsing
- Empty, single, double, and triple arguments
- Case-insensitive handling
- Whitespace trimming

**TestFilterAndRankGenerators** - Search functionality
- Exact matches
- Prefix matches (e.g., "ip" → ipv4, ipv6)
- Substring matches
- Case-insensitive search
- Fallback to all generators

**TestCallGenerator** - Generator invocation
- No-argument generators (uuid, ipv4, etc.)
- Length-based generators (string, email, etc.)
- Range-based generators (date, time, etc.)
- Special generators (password with flags)

**TestGetSubtitle** - UI subtitle generation
- Different subtitle formats for each category
- Parameter display

**TestGeneratorCategories** - Configuration validation
- All generators categorized exactly once
- No duplicate categorization
- All categories reference valid generators

**TestGeneratorConsistency** - Integration testing
- LENGTH_ONLY generators accept length
- RANGE_SUPPORT generators accept ranges
- NO_ARGS generators work without parameters

**TestEdgeCases** - Error handling
- Invalid input handling
- Uniqueness of generated values

## Coverage

Current test coverage: **96% overall**

- `src/generators.py`: **100%** - All generators fully tested
- `src/main.py`: **80%** - Core logic tested (untested parts are Alfred workflow integration)
- `tests/test_generators.py`: **99%**
- `tests/test_main.py`: **95%**

## Test Philosophy

1. **Validation over mocking** - Tests validate actual output formats rather than mocking internals
2. **Checksum verification** - Generators with checksums (IMEI, ISBN) are validated against algorithms
3. **Range testing** - Date/time generators tested for boundary conditions
4. **Format testing** - Regular expressions validate output formats
5. **Uniqueness testing** - Random generators verified to produce different values

## Adding New Tests

When adding a new generator:

1. Add test class to `test_generators.py`
2. Test basic functionality (length, format)
3. Test with custom parameters
4. Validate output format with regex
5. Add to appropriate category in `src/main.py`
6. Add category test to `test_main.py`

Example:
```python
def test_new_generator_format(self):
    result = new_generator()
    self.assertRegex(result, r'^expected-pattern$')

def test_new_generator_custom_length(self):
    result = new_generator(20)
    self.assertEqual(len(result), 20)
```
