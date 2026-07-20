# System Imports
from unittest.mock import patch
import unittest
import io

# Local Imports
from individual import Individual
from family import Family


class Test_US25_UniqueChildrenNames(unittest.TestCase):

    # Test Cases:
    # 1: Two children, same name and same birth date (FAIL)
    # 2: Two children, same name, different birth dates (PASS)
    # 3: Two children, different names, same birth date (PASS)
    # 4: Child missing birthday is ignored, not counted (PASS)
    # 5: Single child (PASS)

    def _make_child(self, uid, name, birthday):
        child = Individual()
        child.uid = uid
        child.name = name
        child.gender = 'F'
        child.birthday = birthday
        child.add_child('F1')
        return child
    # End _make_child

    def test_same_name_same_birthdate_fails(self):
        child1 = self._make_child('I01', 'Alice /Carter/', '1 JAN 1980')
        child2 = self._make_child('I02', 'Alice /Carter/', '1 JAN 1980')
        individuals = [child1, child2]

        fam = Family()
        fam.uid = 'F1'
        fam.add_children('I01')
        fam.add_children('I02')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_unique_children_names(individuals)

            self.assertEqual(fake_out.getvalue(), 'ERROR: US25: Family ID F1 has more than one child named Alice /Carter/ born on 1980-01-01!\n')
            self.assertEqual(result, False)
        # End with
    # End test_same_name_same_birthdate_fails

    def test_same_name_different_birthdate_passes(self):
        child1 = self._make_child('I01', 'Alice /Carter/', '1 JAN 1980')
        child2 = self._make_child('I02', 'Alice /Carter/', '1 JAN 1982')
        individuals = [child1, child2]

        fam = Family()
        fam.uid = 'F1'
        fam.add_children('I01')
        fam.add_children('I02')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_unique_children_names(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_same_name_different_birthdate_passes

    def test_different_name_same_birthdate_passes(self):
        child1 = self._make_child('I01', 'Alice /Carter/', '1 JAN 1980')
        child2 = self._make_child('I02', 'Bob /Carter/', '1 JAN 1980')
        individuals = [child1, child2]

        fam = Family()
        fam.uid = 'F1'
        fam.add_children('I01')
        fam.add_children('I02')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_unique_children_names(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_different_name_same_birthdate_passes

    def test_child_without_birthday_not_counted(self):
        child1 = self._make_child('I01', 'Alice /Carter/', '1 JAN 1980')

        child2 = Individual()
        child2.uid = 'I02'
        child2.name = 'Alice /Carter/'
        child2.gender = 'F'
        child2.add_child('F1')

        individuals = [child1, child2]

        fam = Family()
        fam.uid = 'F1'
        fam.add_children('I01')
        fam.add_children('I02')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_unique_children_names(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_child_without_birthday_not_counted

    def test_single_child_passes(self):
        child1 = self._make_child('I01', 'Alice /Carter/', '1 JAN 1980')
        individuals = [child1]

        fam = Family()
        fam.uid = 'F1'
        fam.add_children('I01')

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_unique_children_names(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_single_child_passes

# End Test_US25_UniqueChildrenNames


if __name__ == '__main__':
    unittest.main()
# End if
