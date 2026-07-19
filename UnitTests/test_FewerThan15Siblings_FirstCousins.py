import unittest
from family import Family


class TestUS15US19(unittest.TestCase):

    def test_us15_valid_family_with_14_children(self):
        # US15: A family with 14 children is valid because it has fewer than 15 siblings
        children = [f"I{i}" for i in range(1, 15)]
        family = Family(uid="F1", husband_id="I100", wife_id="I101", children=children)

        result = family.validate_fewer_than_15_siblings()
        self.assertTrue(result)

    def test_us15_invalid_family_with_15_children(self):
        # US15: A family with 15 children is invalid
        children = [f"I{i}" for i in range(1, 16)]
        family = Family(uid="F1", husband_id="I100", wife_id="I101", children=children)

        result = family.validate_fewer_than_15_siblings()
        self.assertFalse(result)

    def test_us19_first_cousins_married(self):
        # I3 and I4 are siblings.
        # I6 is child of I3.
        # I8 is child of I4.
        # I6 and I8 are first cousins, so they should not marry.
        families = [
            Family(uid="F1", husband_id="I1", wife_id="I2", children=["I3", "I4"]),
            Family(uid="F2", husband_id="I3", wife_id="I5", children=["I6"]),
            Family(uid="F3", husband_id="I4", wife_id="I7", children=["I8"]),
            Family(uid="F4", husband_id="I6", wife_id="I8", children=[])
        ]

        result = families[3].validate_first_cousins_should_not_marry(families)
        self.assertFalse(result)

    def test_us19_valid_marriage_not_cousins(self):
        # I5 and I8 do not share grandparents, so this marriage is valid.
        families = [
            Family(uid="F1", husband_id="I1", wife_id="I2", children=["I3"]),
            Family(uid="F2", husband_id="I3", wife_id="I4", children=["I5"]),
            Family(uid="F3", husband_id="I6", wife_id="I7", children=["I8"]),
            Family(uid="F4", husband_id="I5", wife_id="I8", children=[])
        ]

        result = families[3].validate_first_cousins_should_not_marry(families)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
