# System Imports
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


class Test_US30_ListLivingMarried(unittest.TestCase):

    # Test Cases:
    # 1: Living, married -> included
    # 2: Living, never married -> NOT included
    # 3: Deceased, married -> NOT included
    # 4: No qualifying individuals -> returns empty list
    # 5: Multiple qualifying individuals -> all returned

    def setUp(self):
        self.validator = GEDCOM_Validator()
    # End setUp

    def test_living_married_included(self):
        indi = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985', spouse_fams=['F1'])
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_living_married()

        self.assertIn(indi, result)
    # End test_living_married_included

    def test_living_unmarried_excluded(self):
        indi = make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1990')
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_living_married()

        self.assertNotIn(indi, result)
    # End test_living_unmarried_excluded

    def test_deceased_married_excluded(self):
        indi = make_individual('I03', 'Bob /Taylor/', 'M', '15 MAR 1950', death='20 JUN 2000', spouse_fams=['F1'])
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_living_married()

        self.assertNotIn(indi, result)
    # End test_deceased_married_excluded

    def test_no_qualifying_individuals_returns_empty(self):
        indi = make_individual('I04', 'Noah /Carter/', 'M', '7 APR 2019')
        self.validator.individuals = [indi]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_living_married()

        self.assertEqual(result, [])
    # End test_no_qualifying_individuals_returns_empty

    def test_multiple_qualifying_individuals_all_returned(self):
        indi1 = make_individual('I05', 'Alice /Smith/', 'F', '10 JAN 1980', spouse_fams=['F2'])
        indi2 = make_individual('I06', 'Bob /Jones/', 'M', '22 NOV 1975', spouse_fams=['F2'])
        # Non-qualifying: unmarried, deceased
        indi3 = make_individual('I07', 'Carol /Adams/', 'F', '5 MAR 1970')
        indi4 = make_individual('I08', 'Dave /Hill/', 'M', '1 JUN 1960', death='1 JAN 2020', spouse_fams=['F3'])
        self.validator.individuals = [indi1, indi2, indi3, indi4]

        with patch('sys.stdout', new=io.StringIO()):
            result = self.validator.list_living_married()

        self.assertIn(indi1, result)
        self.assertIn(indi2, result)
        self.assertNotIn(indi3, result)
        self.assertNotIn(indi4, result)
        self.assertEqual(len(result), 2)
    # End test_multiple_qualifying_individuals_all_returned

# End Test_US30_ListLivingMarried


if __name__ == '__main__':
    unittest.main()
# End if
