# System Imports
from unittest.mock import patch
import unittest
import io
import sys
import os

# Make the parent directory importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Local Imports
from individual import Individual
from family import Family

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

def make_family(uid, married, husband_id, wife_id, children=None):
    fam = Family()
    fam.uid = uid
    fam.married = married
    fam.husband_id = husband_id
    fam.wife_id = wife_id

    if (children is not None):
        for child in children:
            fam.add_children(child)
        # End for
    # End if

    return fam
# End make_family


class Test_US10_MarriageUnderAge14(unittest.TestCase):

    # Test Cases:
    # 1: No parent was under age 14 at time of marriage
    # 2: Wife was under age 14 at time of marriage
    # 3: Husband was under age 14 at time of marriage
    # 4: Both parents were under age 14 at time of marriage

    def test_no_parent_under_14(self):
        husband = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985')
        wife = make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1985')

        fam = make_family('F01', '22 JUN 2010', 'I01', 'I02')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_marriage_after_14([husband, wife])
            
            self.assertEqual(True, result)
        # End with
    # End test_no_parent_under_14

    def test_wife_under_14_at_marriage(self):
        husband = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 1985')
        wife = make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 2000')

        fam = make_family('F01', '22 JUN 2010', 'I01', 'I02')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_marriage_after_14([husband, wife])

            self.assertEqual(fake_out.getvalue(), 'ERROR: US10: Wife I02 in family F01 was less than 14 at the time of marriage!\n')
            self.assertEqual(False, result)
        # End with
    # End test_wife_under_14_at_marriage

    def test_husband_under_14_at_marriage(self):
        husband = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 2000')
        wife = make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 1985')

        fam = make_family('F01', '22 JUN 2010', 'I01', 'I02')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_marriage_after_14([husband, wife])

            self.assertEqual(fake_out.getvalue(), 'ERROR: US10: Husband I01 in family F01 was less than 14 at the time of marriage!\n')
            self.assertEqual(False, result)
        # End with
    # End test_husband_under_14_at_marriage

    def test_both_under_14_at_marriage(self):
        husband = make_individual('I01', 'James /Taylor/', 'M', '15 MAR 2000')
        wife = make_individual('I02', 'Charlotte /Taylor/', 'F', '01 MAY 2000')

        fam = make_family('F01', '22 JUN 2010', 'I01', 'I02')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_marriage_after_14([husband, wife])

            self.assertEqual(fake_out.getvalue(), 'ERROR: US10: Husband I01 in family F01 was less than 14 at the time of marriage!\n'
                                                  'ERROR: US10: Wife I02 in family F01 was less than 14 at the time of marriage!\n')
            self.assertEqual(False, result)
        # End with
    # End test_both_under_14_at_marriage

# End Test_US10_MarriageUnderAge14


if __name__ == '__main__':
    unittest.main()
# End if
