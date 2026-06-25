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
    # Validators
    #
    ###########################################################################

    def validate_birth_before_marriage(self, individuals):
        result = True

        husband = next(filter(lambda indi: indi.uid == self._husband_id, individuals), None)
        wife = next(filter(lambda indi: indi.uid == self._wife_id, individuals), None)

        if husband is not None:
            if husband.birthday >= self._married:
                print(f'ERROR: Husband ID {self._husband_id} was married before their birthday!')
                result = False
        else:
            print(f'ERROR: Husband ID {self._husband_id} does not exist in the list of individuals!')
            result = False

        if wife is not None:
            if wife.birthday >= self._married:
                print(f'ERROR: Wife ID {self._wife_id} was married before their birthday!')
                result = False
        else:
            print(f'ERROR: Wife ID {self._wife_id} does not exist in the list of individuals!')
            result = False

        return result
    # End validate_birth_before_marriage

    def validate_children_birth_dates(self, individuals):
        result = True

        for child_id in self._children:
            child = next(filter(lambda indi: indi.uid == child_id, individuals), None)

            if child is None:
                print(f'ERROR: Child ID {child_id} does not exist in the list of individuals!')
                result = False
                continue

            if child.birthday is None:
                continue

            if self._married is not None and child.birthday < self._married:
                print(f'ERROR: Child ID {child_id} was born before the marriage of their parents in family {self._uid}!')
                result = False

            if self._divorced is not None:
                nine_months_after_divorce = self._divorced + timedelta(days=274)
                if child.birthday > nine_months_after_divorce:
                    print(f'ERROR: Child ID {child_id} was born more than 9 months after the divorce of their parents in family {self._uid}!')
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
                print(f'ERROR: Family ID {self._uid} has more than five children born on {birth_date}!')
                result = False
            # End if
        # End for

        return result
    # End validate_multiple_births

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
                print(f'ERROR: Family ID {self._uid} has more than five children born on {birth_date}!')
                result = False
            # End if
        # End for

        return result
    # End validate_multiple_births

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

    def validate_dates_before_current_date(self, individuals):
        result = True

        current_dt = datetime.now()

        # Check Birthday
        if (self.married is not None):
            if ( self.married > current_dt ):
                print(f'ERROR: Married date for ID {self.uid} is after to the current date!')
                result = False
            # End if
        # End if

        # Check Deathday if exists
        if (self.divorced is not None):
            if ( self.divorced > current_dt ):
                print(f'ERROR: Divorced date for ID {self.uid} is after to the current date!')
                result = False
            # End if
        # End if

        return result
    # End validate_dates_before_current_date

    def validate(self, individuals):
        result = True

        # Validate birth before marriage
        result &= self.validate_birth_before_marriage(individuals)

        # Validate children birth dates
        result &= self.validate_children_birth_dates(individuals)

        # Validate multiple births
        result &= self.validate_multiple_births(individuals)

        # Validate dates are after the current date
        result &= self.validate_dates_before_current_date(individuals)

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
