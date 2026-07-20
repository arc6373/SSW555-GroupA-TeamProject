# System Imports
from unittest.mock import patch
from datetime import datetime
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
    return indi


class Test_US27_IndividualAge(unittest.TestCase):

    # Test Cases:
    # 1: Deceased individual's age is computed from birth to death date
    # 2: Living individual's age is computed from birth date to today
    # 3: print_invidiuals() includes each individual's age and returns the individual list

    def setUp(self):
        self.validator = GEDCOM_Validator()
    # End setUp

    def test_deceased_individual_age(self):
        indi = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1950', death='20 JUN 2000')

        self.assertEqual(indi.age, 50)
    # End test_deceased_individual_age

    def test_living_individual_age(self):
        indi = make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990')

        has_not_passed = (datetime.now().month, datetime.now().day) < (5, 1)
        expected_age = datetime.now().year - 1990 - has_not_passed

        self.assertEqual(indi.age, expected_age)
    # End test_living_individual_age

    def test_print_individuals_includes_age_and_returns_individuals(self):
        indi1 = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1950', death='20 JUN 2000')
        indi2 = make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990')
        self.validator.individuals = [indi1, indi2]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = self.validator.print_invidiuals()

            output = fake_out.getvalue()
            self.assertIn('50', output)
            self.assertIn(str(indi2.age), output)
            self.assertEqual(result, [indi1, indi2])
        # End with
    # End test_print_individuals_includes_age_and_returns_individuals

# End Test_US27_IndividualAge


if __name__ == '__main__':
    unittest.main()
# End if
