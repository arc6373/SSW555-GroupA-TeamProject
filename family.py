# System Imports
from datetime import datetime, timedelta

# Local imports
# None

class Family:

    def __init__(self,
                 uid=None,
                 married=None,
                 divorced=None,
                 husband_id=None,
                 wife_id=None,
                 children=None
        ):
        # Store the fields we need for individuals
        self._uid = uid
        # Dates
        self._married = married
        self._divorced = divorced
        # IDs
        self._husband_id = husband_id
        self._wife_id = wife_id
        # List of children IDs
        self._children = [] if children is None else children
    # End __init__

    ###########################################################################
    #
    # Helpers
    #
    ###########################################################################

    def get_year_difference(self, start_date, end_date):
        # Subtract years, then subtract 1 if the end date hasn't crossed the birthday/anniversary yet
        has_not_passed = (end_date.month, end_date.day) < (start_date.month, start_date.day)
        years = end_date.year - start_date.year - has_not_passed

        return years
    # End get_year_difference

    ###########################################################################
    #
    # Validators
    #
    ###########################################################################

    def validate_birth_before_marriage(self, individuals):
        result = True

        husband = next(filter(lambda indi: indi.uid == self._husband_id, individuals), None)
        wife = next(filter(lambda indi: indi.uid == self._wife_id, individuals), None)

        if husband is not None:
            if husband.birthday >= self._married:
                print(f'ERROR: US02: Husband ID {self._husband_id} was married before their birthday!')
                result = False
        else:
            print(f'ERROR: US02: Husband ID {self._husband_id} does not exist in the list of individuals!')
            result = False

        if wife is not None:
            if wife.birthday >= self._married:
                print(f'ERROR: US02: Wife ID {self._wife_id} was married before their birthday!')
                result = False
        else:
            print(f'ERROR: US02: Wife ID {self._wife_id} does not exist in the list of individuals!')
            result = False

        return result
    # End validate_birth_before_marriage

    def validate_children_birth_dates(self, individuals):
        result = True

        for child_id in self._children:
            child = next(filter(lambda indi: indi.uid == child_id, individuals), None)

            if child is None:
                print(f'ERROR: US08: Child ID {child_id} does not exist in the list of individuals!')
                result = False
                continue

            if child.birthday is None:
                continue

            if self._married is not None and child.birthday < self._married:
                print(f'ERROR: US08: Child ID {child_id} was born before the marriage of their parents in family {self._uid}!')
                result = False

            if self._divorced is not None:
                nine_months_after_divorce = self._divorced + timedelta(days=274)
                if child.birthday > nine_months_after_divorce:
                    print(f'ERROR: US08: Child ID {child_id} was born more than 9 months after the divorce of their parents in family {self._uid}!')
                    result = False

        return result
    # End validate_children_birth_dates

    def validate_multiple_births(self, individuals):
        # US14: No more than five siblings should be born at the same time
        result = True
        birth_date_counts = {}

        for child_id in self._children:
            child = next(filter(lambda indi: indi.uid == child_id, individuals), None)

            if child is None or child.birthday is None:
                continue
            # End if

            birth_date = child.birthday.date()

            if birth_date not in birth_date_counts:
                birth_date_counts[birth_date] = []
            # End if

            birth_date_counts[birth_date].append(child_id)
        # End for

        for birth_date, children in birth_date_counts.items():
            if len(children) > 5:
                print(f'ERROR: US14: Family ID {self._uid} has more than five children born on {birth_date}!')
                result = False
            # End if
        # End for

        return result
    # End validate_multiple_births

    def validate_parents_not_too_old(self, individuals):
        # US12: Mother should be less than 60 years older than her children and
        # father should be less than 80 years older than his children
        result = True

        husband = next(filter(lambda indi: indi.uid == self._husband_id, individuals), None)
        wife = next(filter(lambda indi: indi.uid == self._wife_id, individuals), None)

        for child_id in self._children:
            child = next(filter(lambda indi: indi.uid == child_id, individuals), None)

            if child is None or child.birthday is None:
                continue
            # End if

            if wife is not None and wife.birthday is not None:
                age_diff = self.get_year_difference(wife.birthday, child.birthday)
                if age_diff >= 60:
                    print(f'ERROR: US12: Mother ID {self._wife_id} is 60 or more years older than Child ID {child_id} in family {self._uid}!')
                    result = False
                # End if
            # End if

            if husband is not None and husband.birthday is not None:
                age_diff = self.get_year_difference(husband.birthday, child.birthday)
                if age_diff >= 80:
                    print(f'ERROR: US12: Father ID {self._husband_id} is 80 or more years older than Child ID {child_id} in family {self._uid}!')
                    result = False
                # End if
            # End if
        # End for

        return result
    # End validate_parents_not_too_old

    def validate_correct_gender_for_role(self, individuals):
        # US21: Husband in family should be male and wife in family should be female
        result = True

        husband = next(filter(lambda indi: indi.uid == self._husband_id, individuals), None)
        wife = next(filter(lambda indi: indi.uid == self._wife_id, individuals), None)

        if husband is not None and husband.gender != 'M':
            print(f'ERROR: US21: Husband ID {self._husband_id} is not male in family {self._uid}!')
            result = False
        # End if

        if wife is not None and wife.gender != 'F':
            print(f'ERROR: US21: Wife ID {self._wife_id} is not female in family {self._uid}!')
            result = False
        # End if

        return result
    # End validate_correct_gender_for_role

    def order_siblings_by_age(self, individuals):
        # US28: List siblings in families by decreasing age, oldest siblings first
        siblings = []

        for child_id in self._children:
            child = next(filter(lambda indi: indi.uid == child_id, individuals), None)

            if child is not None and child.birthday is not None:
                siblings.append(child)
            # End if
        # End for

        siblings.sort(key=lambda child: child.birthday)

        return siblings
    # End order_siblings_by_age

    def get_descendants(self, person_id, families):
        # Helper for US17: find all descendants of a person
        descendants = set()

        if person_id is None:
            return descendants
        # End if

        for family in families:
            if family.husband_id == person_id or family.wife_id == person_id:
                for child_id in family.children:
                    descendants.add(child_id)
                    descendants.update(self.get_descendants(child_id, families))
                # End for
            # End if
        # End for

        return descendants
    # End get_descendants

    def validate_no_marriages_to_descendants(self, families):
        # US17: Parents should not marry any of their descendants
        result = True

        husband_descendants = self.get_descendants(self._husband_id, families)
        wife_descendants = self.get_descendants(self._wife_id, families)

        if self._wife_id in husband_descendants:
            print(f'ERROR: US17: Husband ID {self._husband_id} is married to descendant Wife ID {self._wife_id} in family {self._uid}!')
            result = False
        # End if

        if self._husband_id in wife_descendants:
            print(f'ERROR: US17: Wife ID {self._wife_id} is married to descendant Husband ID {self._husband_id} in family {self._uid}!')
            result = False
        # End if

        return result
    # End validate_no_marriages_to_descendants

    def get_parents(self, person_id, families):
        # Helper for US20 and US19: find parents of a person
        parents = set()

        if person_id is None:
            return parents
        # End if

        for family in families:
            if person_id in family.children:
                if family.husband_id is not None:
                    parents.add(family.husband_id)
                # End if

                if family.wife_id is not None:
                    parents.add(family.wife_id)
                # End if
            # End if
        # End for

        return parents
    # End get_parents

    def get_siblings(self, person_id, families):
        # Helper for US20: find siblings of a person
        siblings = set()

        if person_id is None:
            return siblings
        # End if

        for family in families:
            if person_id in family.children:
                for child_id in family.children:
                    if child_id != person_id:
                        siblings.add(child_id)
                    # End if
                # End for
            # End if
        # End for

        return siblings
    # End get_siblings

    def get_aunts_uncles(self, person_id, families):
        # Helper for US20: aunts/uncles are siblings of a person's parents
        aunts_uncles = set()
        parents = self.get_parents(person_id, families)

        for parent_id in parents:
            aunts_uncles.update(self.get_siblings(parent_id, families))
        # End for

        return aunts_uncles
    # End get_aunts_uncles

    def validate_aunts_uncles(self, families):
        # US20: Aunts and uncles should not marry their nieces or nephews
        result = True

        husband_aunts_uncles = self.get_aunts_uncles(self._husband_id, families)
        wife_aunts_uncles = self.get_aunts_uncles(self._wife_id, families)

        if self._wife_id in husband_aunts_uncles:
            print(f'ERROR: US20: Husband ID {self._husband_id} is married to aunt/uncle Wife ID {self._wife_id} in family {self._uid}!')
            result = False
        # End if

        if self._husband_id in wife_aunts_uncles:
            print(f'ERROR: US20: Wife ID {self._wife_id} is married to aunt/uncle Husband ID {self._husband_id} in family {self._uid}!')
            result = False
        # End if

        return result
    # End validate_aunts_uncles

    def validate_fewer_than_15_siblings(self):
        # US15: There should be fewer than 15 siblings in a family
        result = True

        if len(self._children) >= 15:
            print(f'ERROR: US15: Family ID {self._uid} has 15 or more siblings!')
            result = False
        # End if

        return result
    # End validate_fewer_than_15_siblings

    def get_grandparents(self, person_id, families):
        # Helper for US19: find grandparents of a person
        grandparents = set()
        parents = self.get_parents(person_id, families)

        for parent_id in parents:
            grandparents.update(self.get_parents(parent_id, families))
        # End for

        return grandparents
    # End get_grandparents

    def validate_first_cousins_should_not_marry(self, families):
        # US19: First cousins should not marry one another
        result = True

        husband_grandparents = self.get_grandparents(self._husband_id, families)
        wife_grandparents = self.get_grandparents(self._wife_id, families)

        common_grandparents = husband_grandparents.intersection(wife_grandparents)

        if len(common_grandparents) > 0:
            print(f'ERROR: US19: Husband ID {self._husband_id} and Wife ID {self._wife_id} are first cousins in family {self._uid}!')
            result = False
        # End if

        return result
    # End validate_first_cousins_should_not_marry

    def validate_no_sibling_marriage(self, individuals):
        # US18: Siblings should not marry one another
        result = True

        husband = next(filter(lambda indi: indi.uid == self._husband_id, individuals), None)
        wife = next(filter(lambda indi: indi.uid == self._wife_id, individuals), None)

        if husband is None or wife is None:
            return result
        # End if

        # Loop through the husband's child families and check if the wife is a child in the same family
        for fam_id in husband.child:
            if fam_id in wife.child:
                print(f'ERROR: US18: Family ID {self._uid} has married siblings from family {fam_id}!')
                result = False
                break
            # End if
        # End for

        return result
    # End validate_no_sibling_marriage

    def validate(self, individuals):
        result = True

        # Validate birth before marriage
        result &= self.validate_birth_before_marriage(individuals)

        # Validate children birth dates
        result &= self.validate_children_birth_dates(individuals)

        # Validate multiple births
        result &= self.validate_multiple_births(individuals)

        # Validate parents not too old
        result &= self.validate_parents_not_too_old(individuals)

        # Validate correct gender for role
        result &= self.validate_correct_gender_for_role(individuals)

        # Validate no sibling marriages
        result &= self.validate_no_sibling_marriage(individuals)

        # Validate fewer than 15 siblings
        result &= self.validate_fewer_than_15_siblings()

        return result
    # End validate

    ###########################################################################
    #
    # Getters and Setters
    #
    ###########################################################################

    def set_tag_value(self, tag, value):
        # Since we are processing GEDCOM tags
        # This method will take in a tag and value abd assign it to the
        # proper python variable
        pass

        if (tag == 'FAM'):
            self.uid = value

        elif (tag == 'MARR'):
            self.married = value

        elif (tag == 'DIV'):
            self.divorced = value

        elif (tag == 'HUSB'):
            self.husband_id = value

        elif (tag == 'WIFE'):
            self.wife_id = value

        elif (tag == 'CHIL'):
            self.add_children(value)

        else:
            print(f'Unknown tag for family {tag}')
        # End if-elif-else
    # End set_tag_value

    @property
    def uid(self):
        return self._uid
    # End uid

    @uid.setter
    def uid(self, value):
        self._uid = value
    # End uid setter

    @property
    def married(self):
        return self._married
    # End married

    @married.setter
    def married(self, value):
        # The married will be converted from a string to a datetime obj
        self._married = datetime.strptime(value, "%d %b %Y")
    # End married setter

    @property
    def divorced(self):
        return self._divorced
    # End divorced

    @divorced.setter
    def divorced(self, value):
        # The divorced will be converted from a string to a datetime obj
        self._divorced = datetime.strptime(value, "%d %b %Y")
    # End divorced setter

    @property
    def husband_id(self):
        return self._husband_id
    # End husband_id

    @husband_id.setter
    def husband_id(self, value):
        self._husband_id = value
    # End husband_id setter

    @property
    def wife_id(self):
        return self._wife_id
    # End wife_id

    @wife_id.setter
    def wife_id(self, value):
        self._wife_id = value
    # End wife_id setter

    @property
    def children(self):
        return self._children
    # End child

    @children.setter
    def children(self, value):
        self._children = value
    # End child setter

    def add_children(self, value):
        self._children.append(value)
    # End add_child

# End individual
