# System Imports
from datetime import datetime

# Local imports
# None

class Individual:

    def __init__(self,
                 uid=None,
                 name=None,
                 gender=None,
                 birthday=None,
                 death=None,
                 child=None,
                 spouse=None
        ):
        # Store the fields we need for individuals
        self._uid = uid
        self._name = name

        self._gender = gender

        self._birthday = birthday
        self._age = None
        self._alive = None
        self._death = death

        self._child = [] if child is None else child
        self._spouse = [] if spouse is None else spouse
    # End __init__

    ###########################################################################
    #
    # Validators
    #
    ###########################################################################

    def validate_death_after_birth(self):
        result = True

        if self._death is not None and self._birthday is not None:

            birthday = datetime.strptime(self._birthday, "%d %b %Y")
            death = datetime.strptime(self._death, "%d %b %Y")
            
            if death < birthday:
                print(f'ERROR: Individual ID {self._uid} has a death date that precedes their birth date!')
                result = False
            # End if
        # End if

        return result
    # End validate_death_after_birth

    def validate_less_than_150(self):
        result = True

        # Check if the age of the individual is less than 150!
        if (self.age >= 150):
            print(f'ERROR: ID {self.uid} is over 150 years old!')
            result = False
        # End if

        return result
    # End validate_less_than_150

    def validate(self):
        result = True
        
        result &= self.validate_less_than_150()
        result &= self.validate_death_after_birth()

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
        if (tag == 'INDI'):
            self.uid = value

        elif (tag == 'NAME'):
            self.name = value

        elif (tag == 'SEX'):
            self.gender = value

        elif (tag == 'BIRT'):
            self.birthday = value

        elif (tag == 'DEAT'):
            self.death = value

        elif (tag == 'FAMC'):
            self.add_child(value)

        elif (tag == 'FAMS'):
            self.add_spouse(value)

        else:
            print(f'Unknown tag for individual {tag}')
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
    def name(self):
        return self._name
    # End name

    @name.setter
    def name(self, value):
        self._name = value
    # End name setter

    @property
    def gender(self):
        return self._gender
    # End gender

    @gender.setter
    def gender(self, value):
        self._gender = value
    # End gender setter

    @property
    def birthday(self):
        return self._birthday
    # End birthday

    @birthday.setter
    def birthday(self, value):
        # The birthday will be converted from a string to a datetime obj
        self._birthday = value
    # End birthday setter

    @property
    def age(self):
        # Calculate the age of the individual
        birthday = datetime.strptime(self._birthday, "%d %b %Y")

        if (self._death is None):
            current_dt = datetime.now()
            self._age = self.get_year_difference(birthday, current_dt)
        else:
            death = datetime.strptime(self._death, "%d %b %Y")
            self._age = self.get_year_difference(birthday, death)
        # End if-else

        return self._age
    # End age

    @age.setter
    def age(self, value):
        self._age = value
    # End age setter

    @property
    def alive(self):
        # Check to see if a death date is listed, if yes then the indiviudal
        # is reported as dead
        if (self._death is not None):
            self._alive = False
        else:
            self._alive = True
        # End if-else

        return self._alive
    # End alive

    @alive.setter
    def alive(self, value):
        self._alive = value
    # End alive setter

    @property
    def death(self):
        return self._death
    # End death

    @death.setter
    def death(self, value):
        # The death day will be converted from a string to a datetime obj
        # We check for None just in case
        if (value is None):
            self._death = None
        else:
            self._death = value
        # End if-else
    # End death setter

    @property
    def child(self):
        return self._child
    # End child

    @child.setter
    def child(self, value):
        self._child = list(value)
    # End child setter

    def add_child(self, value):
        self._child.append(value)
    # End add_child

    @property
    def spouse(self):
        return self._spouse
    # End spouse

    @spouse.setter
    def spouse(self, value):
        self._spouse = list(value)
    # End spouse setter

    def add_spouse(self, value):
        self._spouse.append(value)
    # End add_spouse

    # Helpers
    def get_year_difference(self, start_date, end_date):
        # Subtract years, then subtract 1 if the end date hasn't crossed the birthday/anniversary yet
        has_not_passed = (end_date.month, end_date.day) < (start_date.month, start_date.day)
        years = end_date.year - start_date.year - has_not_passed

        return years
    # End get_year_difference

# End individual