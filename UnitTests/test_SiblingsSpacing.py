# System Imports
from unittest.mock import patch
import unittest
import io

# Local Imports
from individual import Individual
from family import Family


class Test_US13_SiblingsSpacing(unittest.TestCase):

    def _make_child(self, uid, birthday):
        child = Individual()
        child.uid = uid
        child.name = f'Child {uid} /Test/'
        child.gender = 'M'
        child.birthday = birthday
        child.add_child('F1')
        return child

    def test_siblings_more_than_8_months_apart_passes(self):
        child1 = self._make_child('I01', '1 JAN 2000')
        child2 = self._make_child('I02', '1 OCT 2000')

        fam = Family()
        fam.uid = 'F1'
        fam.add_children('I01')
        fam.add_children('I02')

        individuals = [child1, child2]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_siblings_spacing(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)

    def test_siblings_less_than_2_days_apart_passes(self):
        child1 = self._make_child('I01', '1 JAN 2000')
        child2 = self._make_child('I02', '2 JAN 2000')

        fam = Family()
        fam.uid = 'F1'
        fam.add_children('I01')
        fam.add_children('I02')

        individuals = [child1, child2]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_siblings_spacing(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)

    def test_siblings_4_months_apart_fails(self):
        child1 = self._make_child('I01', '1 JAN 2000')
        child2 = self._make_child('I02', '1 MAY 2000')

        fam = Family()
        fam.uid = 'F1'
        fam.add_children('I01')
        fam.add_children('I02')

        individuals = [child1, child2]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_siblings_spacing(individuals)

            self.assertEqual(fake_out.getvalue(), 'ERROR: US13: Siblings ID I01 and ID I02 in family F1 have birth dates less than 8 months apart and more than 1 day apart!\n')
            self.assertEqual(result, False)

    def test_no_children_passes(self):
        fam = Family()
        fam.uid = 'F1'
        individuals = []

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_siblings_spacing(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)

    def test_one_child_passes(self):
        child1 = self._make_child('I01', '1 JAN 2000')

        fam = Family()
        fam.uid = 'F1'
        fam.add_children('I01')

        individuals = [child1]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = fam.validate_siblings_spacing(individuals)

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
