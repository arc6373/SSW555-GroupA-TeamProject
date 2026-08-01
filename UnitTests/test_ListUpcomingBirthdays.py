# System Imports
from datetime import datetime, timedelta
from unittest.mock import patch
import unittest
import io
import sys
import os

# Make the parent directory importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Local Imports
from ged_validator import GEDCOM_Validator
from individual import Individual


def make_individual(uid, name, gender, birthday, death=None):
    indi = Individual()
    indi.uid = uid
    indi.name = name
    indi.gender = gender
    indi.birthday = birthday
    if death is not None:
        indi.death = death
    # End if

    return indi
# End make_individual


class Test_US38_ListUpcomingBirthdays(unittest.TestCase):

    # Test Cases:
    # 1: Living person with birthday 15 days from today -> included
    # 2: Living person with birthday 40 days from today -> NOT included
    # 3: Deceased person with upcoming birthday -> NOT included
    # 4: Person whose birthday is today -> included
    # 5: Birthday wraps into next year (near year boundary) -> included
    # 6: Feb 29 birthday in a non-leap "today" year does not crash and is handled as Feb 28

    def setUp(self):
        self.validator = GEDCOM_Validator()
    # End setUp

    def test_birthday_within_30_days_included(self):
        current_dt = datetime.now()

        indi_birthday = current_dt + timedelta(days=15)
        # Use a birth year far enough in the past that the person is alive and plausible
        indi = make_individual('I01', 'James /Taylor/', 'M', indi_birthday.replace(year=1985).strftime("%d %b %Y"))
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_upcoming_birthdays()

        self.assertIn(indi, result)
    # End test_birthday_within_30_days_included

    def test_birthday_beyond_30_days_excluded(self):
        current_dt = datetime.now()

        indi_birthday = current_dt + timedelta(days=40)
        indi = make_individual('I02', 'Charlotte /Taylor/', 'F', indi_birthday.replace(year=1990).strftime("%d %b %Y"))
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_upcoming_birthdays()

        self.assertNotIn(indi, result)
    # End test_birthday_beyond_30_days_excluded

    def test_deceased_person_excluded(self):
        current_dt = datetime.now()

        indi_birthday = current_dt + timedelta(days=10)
        indi = make_individual('I03', 'Bob /Taylor/', 'M', indi_birthday.replace(year=1950).strftime("%d %b %Y"), death='1 JAN 2020')
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_upcoming_birthdays()

        self.assertNotIn(indi, result)
    # End test_deceased_person_excluded

    def test_birthday_today_included(self):
        current_dt = datetime.now()

        indi = make_individual('I04', 'Emma /Carter/', 'F', current_dt.replace(year=1995).strftime("%d %b %Y"))
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_upcoming_birthdays()

        self.assertIn(indi, result)
    # End test_birthday_today_included

    def test_birthday_wraps_into_next_year(self):
        indi = make_individual('I05', 'Noah /Bennett/', 'M', '5 JAN 1990')

        self.validator.individuals = [indi]

        with patch('ged_validator.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 12, 20)

            with patch('sys.stdout', new=io.StringIO()):
                result = self.validator.list_upcoming_birthdays()
            # End with
        # End with

        self.assertIn(indi, result)
    # End test_birthday_wraps_into_next_year

    def test_feb_29_birthday_does_not_crash(self):
        indi = make_individual('I06', 'Leah /Bennett/', 'F', '29 FEB 1988')

        self.validator.individuals = [indi]

        with patch('ged_validator.datetime') as mock_datetime:
            # 2025 is not a leap year
            mock_datetime.now.return_value = datetime(2025, 2, 20)

            with patch('sys.stdout', new=io.StringIO()):
                result = self.validator.list_upcoming_birthdays()
            # End with
        # End with

        self.assertIn(indi, result)
    # End test_feb_29_birthday_does_not_crash

# End Test_US38_ListUpcomingBirthdays


if __name__ == '__main__':
    unittest.main()
# End if
