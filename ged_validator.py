# System Imports
from prettytable import PrettyTable
from datetime import datetime
import sys
import os
import re

# Local imports
from individual import Individual
from family import Family


class GEDCOM_Validator:

    def __init__(self):
        self.valid_tags = {
            'INDI': 0,
            'NAME': 1,
            'SEX':  1,
            'BIRT': 1,
            'DEAT': 1,
            'FAMC': 1,
            'FAMS': 1,
            'FAM':  0,
            'MARR': 1,
            'HUSB': 1,
            'WIFE': 1,
            'CHIL': 1,
            'DIV':  1,
            'DATE': 2,
            'HEAD': 0,
            'TRLR': 0,
            'NOTE': 0
        }

        self.individuals = []
        self.families = []

        self.current_record = None
        self.current_record_type = None
        self.pending_tag = None
    # End __init__

    def check_tag_valid(self, tag, level):
        # Default value is the tag is not valid or 'N'
        ret_val = 'N'

        # Check to see if the tag is in the valid list
        if (tag in self.valid_tags):
            # The tag is valid, does it match the valid level though
            if (level == str(self.valid_tags[tag])):
                ret_val = 'Y'
            # End if
        # End if

        return ret_val
    # End check_tag_valid

    def get_year_difference(self, start_date, end_date):
        # Subtract years, then subtract 1 if the end date hasn't crossed the birthday/anniversary yet
        has_not_passed = (end_date.month, end_date.day) < (start_date.month, start_date.day)
        years = end_date.year - start_date.year - has_not_passed

        return years
    # End get_year_difference

    def print_invidiuals(self):
        # Start the table and add the field names
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

        for individual in self.individuals:
            fields = []
            fields.append(individual.uid)
            fields.append(individual.name)
            fields.append(individual.gender)
            fields.append(individual.birthday.strftime("%Y-%m-%d"))
            fields.append(individual.age)
            fields.append(individual.alive)


            if (individual.death is None):
                fields.append('N/A')
            else:
                fields.append(individual.death.strftime("%Y-%m-%d"))
            # End if-else
            data = individual.child
            fields.append(data if len(data) != 0 else 'N/A')
            data = individual.spouse
            fields.append(data if len(data) != 0 else 'N/A')

            table.add_row(fields)
        # End for

        print(table.get_string())
    # End print_invidiuals

    def print_family(self):
        # Start the table and add the field names
        table = PrettyTable()
        table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]

        for family in self.families:
            fields = []
            fields.append(family.uid)
            fields.append(family.married.strftime("%Y-%m-%d"))

            if (family.divorced is None):
                fields.append('N/A')
            else:
                fields.append(family.divorced.strftime("%Y-%m-%d"))
            # End if-else

            fields.append(family.husband_id)
            result = next(filter(lambda indi: indi.uid == family.husband_id, self.individuals), None)
            fields.append(result.name)
            fields.append(family.wife_id)
            result = next(filter(lambda indi: indi.uid == family.wife_id, self.individuals), None)
            fields.append(result.name)
            fields.append(family.children)

            table.add_row(fields)
        # End for

        print(table.get_string())
    # End print_family

    def print_family_info(self):
        # Print the siblings in order!
        for family in self.families:

            print(f'Family ID {family.uid} Children:')

            ordered_siblings = family.order_siblings_by_age(self.individuals)

            for sibling in ordered_siblings:
                print(f'Child ID {sibling.uid}: Name {sibling.name} - Age {sibling.age}')
            # End for

            print()
        # End for

    # End print_family_info


    def validate_unique_name_and_birthday(self):
        result = True

        # Make a map a list to store
        name_birthday_map = {}

        # Loop through the list of individuals to fill in the map
        for individual in self.individuals:
            key = '{}-{}'.format(
                individual.name,
                individual.birthday.strftime('%Y-%m-%d')
                )

            if (key not in name_birthday_map.keys()):
                name_birthday_map[key] = []
            # End if

            name_birthday_map[key].append(individual)
        # End for

        for key,value in name_birthday_map.items():
            if (len(value) > 1):

                uids = [ind.uid for ind in value]

                print('ERROR: Individual UIDs {} have the same birthday ({}) and same name ({})'.format(
                        ','.join(uids),
                        value[0].birthday.strftime('%Y-%m-%d'),
                        value[0].name
                    ))

                result = False
            # End if
        # End for

        return result
    # End validate_unique_name_and_birthday

    def validate(self):
        print('\n')
        print('INFO: Starting Validations!')

        # Validation result
        result = True

        # First we will want to validate the individuals
        for individual in self.individuals:
            result &= individual.validate()
        # End for

        # Now we will want to validate the families
        for family in self.families:
            result &= family.validate(self.individuals)
        # End for

        # Now validate individuals
        result &= self.validate_unique_name_and_birthday()

        if (result is False):
            print('WARN: Validation failed!')
        else:
            print('INFO: Validation is complete!')
        # End if-else
    # End validate


    def run(self, gedcom_file):
        print(gedcom_file)

        # Check if the input file exists, if it doesnt we stop execution
        if not os.path.exists(gedcom_file):
            print(f'ERROR: Provided file ({gedcom_file}) does not exist!')
            return
        # End if

        # Open the file
        with open(gedcom_file, 'r') as fileh:
            for line in fileh:
                # Remove special chars!
                strip_line = line.strip()

                # First print
                print(f'--> {strip_line}')

                # Split the line by spaces
                split_line = strip_line.split(' ', maxsplit=2)
                level = split_line[0]

                # There are two types of tags that do not match the standard format
                if (('INDI' in line) or ('FAM' in line)) and (level == '0'):
                    arguments = split_line[1]
                    tag = split_line[2]
                else:
                    tag = split_line[1]
                    arguments = split_line[2] if len(split_line) >= 3 else ''
                # End if-else

                # Check if the tag is valid!
                valid = self.check_tag_valid(tag, level)

                # Second print - added newline for readability
                print(f'<-- {level}|{tag}|{valid}|{arguments}\n')

                # Post processing!
                arguments = arguments.strip('@')

                # Build individual/family collections
                if level == '0':

                    # A new L0 title was found, store any active items if we are working
                    # on one
                    if (self.current_record_type == 'INDI'):
                        self.individuals.append(self.current_record)
                    elif (self.current_record_type == 'FAM'):
                        self.families.append(self.current_record)
                    # End if-elif

                    if tag == 'INDI':
                        iid = arguments.strip('@')
                        self.current_record = Individual(uid=iid)
                        self.current_record_type = 'INDI'
                    elif tag == 'FAM':
                        iid = arguments.strip('@')
                        self.current_record = Family(uid=iid)
                        self.current_record_type = 'FAM'
                    else:
                        self.current_record = None
                        self.current_record_type = None
                    # End if-elif-else
                    self.pending_tag = None

                elif level == '1' and self.current_record is not None:
                    if valid == 'Y':
                        if tag in ('BIRT', 'DEAT', 'MARR', 'DIV'):
                            self.pending_tag = tag
                        else:
                            self.current_record.set_tag_value(tag, arguments)
                        # End if-else
                    # End if

                elif level == '2' and tag == 'DATE' and self.pending_tag and self.current_record is not None:
                    self.current_record.set_tag_value(self.pending_tag, arguments)
                    self.pending_tag = None
                # End if-elif
            # End for
        # End with

        # Now print the tables
        print()
        self.print_invidiuals()
        print()
        self.print_family()
        print()
        self.print_family_info()

        # Now we will run validations!
        self.validate()
    # End run

# End GEDCOM_Validator


if __name__ == '__main__':
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(description="The arguments for the GEDCOM Validator.")
    parser.add_argument("-g", "--gedcom", required=True, help="Path to the GEDCOM file to process")
    args = parser.parse_args()

    # Call the run
    gedcom_val = GEDCOM_Validator()
    gedcom_val.run(args.gedcom)
# End if