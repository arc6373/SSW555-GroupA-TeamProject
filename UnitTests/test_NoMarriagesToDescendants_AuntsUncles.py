from unittest.mock import patch
import unittest
import io

from family import Family


class TestUS17US20(unittest.TestCase):

    # -------------------------
    # US17 Tests
    # -------------------------

    def test_us17_parent_married_to_child(self):
        # F1: I1 and I2 are parents of I3
        # F2: I1 is married to I3, which is not allowed
        families = [
            Family(uid="F1", husband_id="I1", wife_id="I2", children=["I3"]),
            Family(uid="F2", husband_id="I1", wife_id="I3", children=[])
        ]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = families[1].validate_no_marriages_to_descendants(families)
            self.assertFalse(result)

    def test_us17_parent_married_to_grandchild(self):
        # F1: I1 and I2 have child I3
        # F2: I3 and I4 have child I5
        # F3: I1 is married to I5, which is not allowed
        families = [
            Family(uid="F1", husband_id="I1", wife_id="I2", children=["I3"]),
            Family(uid="F2", husband_id="I3", wife_id="I4", children=["I5"]),
            Family(uid="F3", husband_id="I1", wife_id="I5", children=[])
        ]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = families[2].validate_no_marriages_to_descendants(families)
            self.assertFalse(result)

    def test_us17_valid_marriage_not_descendant(self):
        # I3 is child of I1 and I2
        # I3 marries I4, who is not a descendant
        families = [
            Family(uid="F1", husband_id="I1", wife_id="I2", children=["I3"]),
            Family(uid="F2", husband_id="I3", wife_id="I4", children=[])
        ]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = families[1].validate_no_marriages_to_descendants(families)
            self.assertTrue(result)

    # -------------------------
    # US20 Tests
    # -------------------------

    def test_us20_uncle_married_to_niece(self):
        # F1: I1 and I2 have children I3 and I4
        # F2: I3 has child I6
        # I4 is uncle/aunt of I6
        # F3: I4 is married to I6, which is not allowed
        families = [
            Family(uid="F1", husband_id="I1", wife_id="I2", children=["I3", "I4"]),
            Family(uid="F2", husband_id="I3", wife_id="I5", children=["I6"]),
            Family(uid="F3", husband_id="I4", wife_id="I6", children=[])
        ]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = families[2].validate_aunts_uncles(families)
            self.assertFalse(result)

    def test_us20_aunt_married_to_nephew(self):
        # F1: I1 and I2 have children I3 and I4
        # F2: I3 has child I6
        # I4 is aunt/uncle of I6
        # F3: I6 is married to I4, which is not allowed
        families = [
            Family(uid="F1", husband_id="I1", wife_id="I2", children=["I3", "I4"]),
            Family(uid="F2", husband_id="I3", wife_id="I5", children=["I6"]),
            Family(uid="F3", husband_id="I6", wife_id="I4", children=[])
        ]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = families[2].validate_aunts_uncles(families)
            self.assertFalse(result)

    def test_us20_valid_marriage_not_aunt_or_uncle(self):
        # I6 marries I7, who is unrelated
        families = [
            Family(uid="F1", husband_id="I1", wife_id="I2", children=["I3", "I4"]),
            Family(uid="F2", husband_id="I3", wife_id="I5", children=["I6"]),
            Family(uid="F3", husband_id="I6", wife_id="I7", children=[])
        ]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = families[2].validate_aunts_uncles(families)
            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
