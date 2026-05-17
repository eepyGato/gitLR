# ---------------------------------------------------------
# Lab Work №4 - Task 1 (Variant 9)
# Module: person.py
# Purpose: Define person classes for personal data storage
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------


class PrintableMixin:
    """Mixin to print all persons passed as an argument."""

    @staticmethod
    def print_all(persons):
        """
        Print all persons passed as a list using their __str__ method.

        Args:
            persons: List of person objects to display
        """
        if not persons:
            print("No data available.")
            return

        print("\n" + "=" * 60)
        print("All Persons:")
        print("=" * 60)

        for index, person in enumerate(persons, 1):
            print(f"{index}. {person}")

        print("=" * 60 + "\n")


class Person(PrintableMixin):
    """Base class for a person with surname, gender and height."""

    all_persons = []

    def __init__(self, last_name: str, gender: str, height: float):
        """
        Initialize a person object.

        Args:
            last_name (str): Person's surname
            gender (str): Gender ('M' for male, 'F' for female)
            height (float): Height in centimeters
        """
        self.last_name = last_name  # uses property setter
        self.gender = gender.upper()  # dynamic attribute
        self.height = height  # dynamic attribute
        Person.all_persons.append(self)  # add to static list

    def __str__(self) -> str:
        """
        String representation of person.

        Returns:
            str: Formatted person information
        """
        gender_str = "Female" if self.gender == "F" else "Male"
        return f"{self.last_name:<15} | Gender: {gender_str:<6} | Height: {self.height} cm"

    @property
    def last_name(self) -> str:
        """
        Getter for last_name property.

        Returns:
            str: Person's surname
        """
        return self._last_name

    @last_name.setter
    def last_name(self, name: str):
        """
        Setter for last_name property.
        Automatically converts to title case.

        Args:
            name (str): Person's surname
        """
        self._last_name = name.title()

    @classmethod
    def search_by_letter(cls, letter: str) -> list:
        """
        Search persons by first letter of surname.
        Case-insensitive search.

        Args:
            letter (str): First letter to search for

        Returns:
            list: List of persons with matching surname letter
        """
        return [person for person in cls.all_persons
                if person.last_name.upper().startswith(letter.upper())]

    @classmethod
    def search_by_surname(cls, surname: str):
        """
        Search for specific person by exact surname.

        Args:
            surname (str): Full surname to search for

        Returns:
            Person: First person with matching surname or None
        """
        for person in cls.all_persons:
            if person.last_name.lower() == surname.lower():
                return person
        return None

    @classmethod
    def get_average_height_women(cls) -> float | None:
        """
        Calculate average height of all women.

        Returns:
            float: Average height or None if no women found
        """
        women = [person for person in cls.all_persons if person.gender == "F"]

        if women:
            return sum(person.height for person in women) / len(women)
        return None

    @classmethod
    def get_tallest_man(cls):
        """
        Find the tallest man in the person list.

        Returns:
            Person: Tallest man's person or None if no men found
        """
        men = [person for person in cls.all_persons if person.gender == "M"]

        if men:
            return max(men, key=lambda person: person.height)
        return None

    @classmethod
    def check_same_height_pair(cls) -> bool:
        """
        Check if there are at least two people with same height.

        Returns:
            bool: True if pair with same height exists, False otherwise
        """
        heights = [person.height for person in cls.all_persons]

        return len(heights) != len(set(heights))

    @classmethod
    def get_people_with_height(cls, height: float) -> list:
        """
        Get all people with specific height.

        Args:
            height (float): Height in centimeters

        Returns:
            list: List of persons with matching height
        """
        return [person for person in cls.all_persons if person.height == height]


class BusinessPerson(Person, PrintableMixin):
    """
    Extended person class with business information.
    Inherits from Person and PrintableMixin.

    Attributes:
        company (str): Company name
    """

    def __init__(self, last_name: str, gender: str, height: float, company: str):
        """
        Initialize a business person.

        Args:
            last_name (str): Person's surname
            gender (str): Gender ('M' or 'F')
            height (float): Height in centimeters
            company (str): Company name
        """
        super().__init__(last_name, gender, height)
        self.company = company

    def __str__(self) -> str:
        """
        String representation with company information.

        Returns:
            str: Formatted person information with company
        """
        gender_str = "Female" if self.gender == "F" else "Male"
        return (f"{self.last_name:<15} | Gender: {gender_str:<6} | "
                f"Height: {self.height} cm | Company: {self.company}")
