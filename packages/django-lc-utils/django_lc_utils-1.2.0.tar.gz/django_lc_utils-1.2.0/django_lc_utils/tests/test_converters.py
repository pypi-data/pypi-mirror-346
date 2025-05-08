import unittest

from ..converters import (
    clean_html,
    convert_numbers_to_words,
    parse_json_string,
    phone_format,
    snake_case,
)


class TestSnakeCase(unittest.TestCase):
    camel_case_name = "HelloWorld"
    snake_case_name = "hello_world"
    not_snake_case_name = "helloWorld"

    def test_snake_case_pass(self):
        assert snake_case(self.camel_case_name) == self.snake_case_name

    def test_snake_case_fail(self):
        assert snake_case(self.camel_case_name) != self.not_snake_case_name


class TestPhoneFormat(unittest.TestCase):
    phone_number_unformatted = "1234567890"
    phone_number_formatted = "123-456-7890"
    phone_number_int = 1234567890

    def test_phone_format_pass(self):
        assert phone_format(self.phone_number_unformatted) == self.phone_number_formatted

    def test_phone_number_integer_passed(self):
        with self.assertRaises(TypeError):
            phone_format(self.phone_number_int)


class TestCleanHtml(unittest.TestCase):
    hello_world_paragraph = "<p>Hello, World</p>"
    hello_world_script = '<script>alert("Hello World!");</script>'
    custom_sanitizer = {"tags": ["p"]}

    # Test with default sanitizer
    def test_clean_html_paragraph(self):
        assert clean_html(self.hello_world_paragraph) == self.hello_world_paragraph

    def test_clean_html_script(self):
        assert clean_html(self.hello_world_script) == ""

    # Test with invalid input
    def test_clean_html_invalid_input(self):
        assert clean_html("") == ""


class TestNumbersToWords(unittest.TestCase):
    def test_numbers_to_words_int_pass(self):
        assert convert_numbers_to_words(23) == "twenty-three"

    def test_numbers_to_words_float_pass(self):
        assert convert_numbers_to_words(23.3) == "twenty-three point three"

    def test_numbers_to_words_str_pass(self):
        assert convert_numbers_to_words("23") == "twenty-three"

    def test_numbers_to_words_float_as_a_string_pass(self):
        assert convert_numbers_to_words("23.3") == "twenty-three point three"

    def test_numbers_to_words_invalid_input(self):
        assert convert_numbers_to_words("Hello") == "zero"


class TestParseJsonString(unittest.TestCase):
    def test_parse_json_string_dict_pass(self):
        assert parse_json_string('{"Hello":"World"}') == {"Hello": "World"}

    def test_parse_json_string_non_dict_pass(self):
        assert parse_json_string("Hello") == "Hello"

    def test_parse_json_string_int_fail(self):
        with self.assertRaises(TypeError):
            parse_json_string(12)
