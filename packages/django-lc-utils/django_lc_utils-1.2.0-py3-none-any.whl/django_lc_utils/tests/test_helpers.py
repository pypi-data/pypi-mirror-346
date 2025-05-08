import datetime
import random
import unittest

import holidays

from ..helper import (
    clean_phone_number,
    mask_phone_number,
    next_business_day,
    recursive_update,
)


class TestCleanPhoneNumber(unittest.TestCase):
    def test_clean_phone_number_us_no(self):
        assert clean_phone_number("+1(812) 4321-543") == "+1 8124321543"

    def test_clean_phone_number_ind_no(self):
        assert clean_phone_number("+91 996-788-4840") == "+91 9967884840"

    def test_clean_phone_number_no_puntuation(self):
        assert clean_phone_number("1234567890") == "1234567890"


class TestMaskPhoneNumber(unittest.TestCase):
    def test_mask_phone_number(self):
        assert mask_phone_number("1234567890") == "XXXXX67890"


class TestNextBusinessDay(unittest.TestCase):
    monday = datetime.date(2023, 3, 27)
    sunday = datetime.date(2023, 3, 26)
    thanksgiving_holiday = datetime.date(2022, 11, 24)

    def test_next_business_day_sunday(self):
        assert next_business_day(self.sunday) == self.monday

    def test_next_business_day_monday(self):
        assert next_business_day(self.monday) == self.monday

    # def test_next_business_day_holiday(self):
    #     assert next_business_day(self.thanksgiving_holiday) == datetime.date(2022, 11, 25)

    def test_next_business_day_today(self):
        date = datetime.date.today()
        us_holidays = holidays.US()
        while date.isoweekday() > 5 or date in us_holidays:
            date += datetime.timedelta(days=1)
        assert next_business_day() == date

    def test_next_business_day_holiday_random(self):
        us_holidays = holidays.US()
        rand_holiday = random.choice(list(holidays.US(years=datetime.date.today().year).keys()))
        date = rand_holiday
        while date.isoweekday() > 5 or date in us_holidays:
            date += datetime.timedelta(days=1)
        assert next_business_day(rand_holiday) == date

    def test_next_business_day_str_fail(self):
        with self.assertRaises(AttributeError):
            next_business_day("2023-03-27")


class TestRecursiveUpdate(unittest.TestCase):
    base_dict = {"name": "person", "hello": "world", "occupation": "employee"}

    def test_recursive_update_empty_dict(self):
        assert recursive_update({}, self.base_dict) == {
            "name": "person",
            "hello": "world",
            "occupation": "employee",
        }

    def test_recursive_update_contains_a_same_key_value_dict(self):
        assert recursive_update({"name": "person"}, self.base_dict) == {
            "name": "person",
            "hello": "world",
            "occupation": "employee",
        }

    def test_recursive_update_contains_a_same_key_dict(self):
        assert recursive_update({"name": "human"}, self.base_dict) == {
            "name": "person",
            "hello": "world",
            "occupation": "employee",
        }

    def test_recursive_update_contains_a_different_key_dict(self):
        assert recursive_update({"city": "new-york"}, self.base_dict) == {
            "name": "person",
            "hello": "world",
            "occupation": "employee",
            "city": "new-york",
        }

    def test_recursive_update_none_type_passed_to_be_updated(self):
        with self.assertRaises(TypeError):
            recursive_update(None, self.base_dict)

    def test_recursive_update_base_dict_none(self):
        with self.assertRaises(AttributeError):
            recursive_update({}, None)

    def test_recursive_update_both_dict_none(self):
        with self.assertRaises(AttributeError):
            recursive_update(None, None)
