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

    def validate(self, individuals):
        valid = True

        for child_id in self._children:
            child = next((i for i in individuals if i.uid == child_id), None)
            if child is None or child.birthday is None:
                continue

            if self._married is not None and child.birthday < self._married:
                print(f'ERROR: Child {child_id} ({child.name}) in family {self._uid} was born {child.birthday.strftime("%Y-%m-%d")} before parents\' marriage on {self._married.strftime("%Y-%m-%d")}')
                valid = False

            if self._divorced is not None:
                nine_months_after_divorce = self._divorced + timedelta(days=274)
                if child.birthday > nine_months_after_divorce:
                    print(f'ERROR: Child {child_id} ({child.name}) in family {self._uid} was born {child.birthday.strftime("%Y-%m-%d")} more than 9 months after parents\' divorce on {self._divorced.strftime("%Y-%m-%d")}')
                    valid = False

        return valid
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