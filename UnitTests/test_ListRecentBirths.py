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


def make_individual(uid, name, gender, birthday, death=None, spouse_fams=None):
    indi = Individual()
    indi.uid = uid
    indi.name = name
    indi.gender = gender
    indi.birthday = birthday
    if death is not None:
        indi.death = death
    # End if

    if spouse_fams:
        for fam_id in spouse_fams:
            indi.add_spouse(fam_id)
        # End for
    # End if

    return indi
# End make_individual


class Test_US35_ListRecentBirths(unittest.TestCase):

    # Test Cases:
    # 1: No recent births
    # 2: One recent birth
    # 3: Two recent births

    def setUp(self):
        self.validator = GEDCOM_Validator()
    # End setUp

    def test_no_recent_births(self):
        self.validator.individuals = []

        indi1 = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985')
        self.validator.individuals.append(indi1)

        indi2 = make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990')
        self.validator.individuals.append(indi2)

        indi3 = make_individual('I03', 'Bob /Taylor/', 'M', '15 MAR 2000')
        self.validator.individuals.append(indi3)

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.list_recent_births()
            
            self.assertEqual([], result)
        # End with
    # End test_no_dead_parents

    def test_one_recent_birth(self):
        current_dt = datetime.now()

        self.validator.individuals = []

        indi1 = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985')
        self.validator.individuals.append(indi1)

        indi2_birthday = current_dt - timedelta(days=1)
        indi2 = make_individual('I02', 'Charlotte /Taylor/', 'F', indi2_birthday.strftime("%d %b %Y"))
        self.validator.individuals.append(indi2)

        indi3 = make_individual('I03', 'Bob /Taylor/', 'M', '15 MAR 2000')
        self.validator.individuals.append(indi3)

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.list_recent_births()

            self.assertIn(indi2, result)
        # End with
    # End test_one_recent_birth

    def test_two_recent_births(self):\
        # Using the current datetime object will make this test continue to pass in the future by
        # using dynamic dates and birthdays
        current_dt = datetime.now()

        self.validator.individuals = []

        indi1 = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985')
        self.validator.individuals.append(indi1)

        indi2_birthday = current_dt - timedelta(days=1)
        indi2 = make_individual('I02', 'Charlotte /Taylor/', 'F', indi2_birthday.strftime("%d %b %Y"))
        self.validator.individuals.append(indi2)

        indi3_birthday = current_dt - timedelta(days=30)
        indi3 = make_individual('I03', 'Bob /Taylor/', 'M', indi3_birthday.strftime("%d %b %Y"))
        self.validator.individuals.append(indi3)

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.list_recent_births()

            self.assertIn(indi2, result)
            self.assertIn(indi3, result)
        # End with
    # End test_two_recent_births

# End Test_US35_ListRecentBirths


if __name__ == '__main__':
    unittest.main()
# End if
