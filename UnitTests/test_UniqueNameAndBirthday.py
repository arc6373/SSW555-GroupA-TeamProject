# System Imports
from unittest.mock import patch
import unittest
import io

# Local Imports
from ged_validator import GEDCOM_Validator
from individual import Individual


class Test_US23_UniqueNameAndBirthday(unittest.TestCase):

    # Test Cases:
    # 1: Two individuals with matching birthday and name (FAIL)
    # 2: Individuals with matching birthday but unique name (PASS)
    # 3: Individuals with matching name but unique birthday (PASS)


    def test_matching_names_and_birthday(self):
        # Create the UUT
        gedcom_val = GEDCOM_Validator()

        # Create some test fields
        individual = Individual()
        individual.uid = 'I01'
        individual.name = 'Thomas /Carter/'
        individual.gender = 'M'
        individual.birthday = '5 MAY 1950'
        individual.death = '1 JAN 1940'
        # Add it to the gedcom validator
        gedcom_val.individuals.append(individual)

        # Adjust the UID for unique IDs
        individual2 = Individual()
        individual2.uid = 'I02'
        individual2.name = 'Thomas /Carter/'
        individual2.gender = 'M'
        individual2.birthday = '5 MAY 1950'
        individual2.death = '1 JAN 1940'
        gedcom_val.individuals.append(individual2)

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = gedcom_val.validate_unique_name_and_birthday()

            self.assertEqual(fake_out.getvalue(), 'ERROR: Individual UIDs I01,I02 have the same birthday (1950-05-05) and same name (Thomas /Carter/)\n')
            self.assertEqual(result, False)
        # End with
    # End test_death_before_birth

    def test_unique_name_matching_birthday(self):
        # Create the UUT
        gedcom_val = GEDCOM_Validator()

        # Create some test fields
        individual = Individual()
        individual.uid = 'I01'
        individual.name = 'Bob /Carter/'
        individual.gender = 'M'
        individual.birthday = '5 MAY 1950'
        individual.death = '1 JAN 1940'
        # Add it to the gedcom validator
        gedcom_val.individuals.append(individual)

        # Adjust the UID for unique IDs
        individual2 = Individual()
        individual2.uid = 'I02'
        individual2.name = 'Thomas /Carter/'
        individual2.gender = 'M'
        individual2.birthday = '5 MAY 1950'
        individual2.death = '1 JAN 1940'
        gedcom_val.individuals.append(individual2)

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = gedcom_val.validate_unique_name_and_birthday()

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_death_after_birth

    def test_matching_name_unique_birthday(self):
        # Create the UUT
        gedcom_val = GEDCOM_Validator()

        # Create some test fields
        individual = Individual()
        individual.uid = 'I01'
        individual.name = 'Thomas /Carter/'
        individual.gender = 'M'
        individual.birthday = '5 MAY 1950'
        individual.death = '1 JAN 1940'
        # Add it to the gedcom validator
        gedcom_val.individuals.append(individual)

        # Adjust the UID for unique IDs
        individual2 = Individual()
        individual2.uid = 'I02'
        individual2.name = 'Thomas /Carter/'
        individual2.gender = 'M'
        individual2.birthday = '7 AUG 1952'
        individual2.death = '1 JAN 1940'
        gedcom_val.individuals.append(individual2)

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = gedcom_val.validate_unique_name_and_birthday()

            self.assertEqual(fake_out.getvalue(), '')
            self.assertEqual(result, True)
        # End with
    # End test_no_death_date

# End Test_US23_UniqueNameAndBirthday


if __name__ == '__main__':
    unittest.main()
# End if
