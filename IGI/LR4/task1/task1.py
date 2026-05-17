# ---------------------------------------------------------
# Lab Work №4 - Task 1 (Variant 9)
# Module: task1.py
# Purpose: Main interface for personal data management
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

from task1.person import Person
from task1.storage_csv import save_to_csv, load_from_csv
from task1.storage_pickle import save_to_pickle, load_from_pickle
from utils.inputValidator import input_with_validator, input_data

DESCRIPTION = """
╔════════════════════════════════════════════════════════════╗
║              Personal Data Management System               ║
║                                                            ║
║  This program manages personal information including:      ║
║  • Surname, Gender, and Height of individuals              ║
║                                                            ║
║  Capabilities:                                             ║
║  ✓ Add new person's data                                   ║
║  ✓ Calculate average height of women                       ║
║  ✓ Find tallest man's surname                              ║
║  ✓ Check for people with same height                       ║
║  ✓ Display information about searched person               ║
║  ✓ Save/Load data from CSV and Pickle formats              ║
╚════════════════════════════════════════════════════════════╝
"""


def display_menu():
    """
    Display main menu with all available options.
    """
    print("\n" + "=" * 60)
    print("Person Management Menu")
    print("=" * 60)
    print("1.  Add new person")
    print("2.  Find by surname")
    print("3.  Find by first letter")
    print("4.  Calculate average height of women")
    print("5.  Find tallest man")
    print("6.  Check for people with same height")
    print("7.  Display searched person info")
    print("8.  Show all persons")
    print("9.  Save to CSV")
    print("10. Load from CSV")
    print("11. Save to Pickle")
    print("12. Load from Pickle")
    print("0.  Exit\n")


def add_person():
    print("\n" + "-" * 40)
    print("Add New Person")
    print("-" * 40)

    surname = input_with_validator(
        "Enter surname (letters only): ",
        str.isalpha
    )

    while True:
        gender = input("Enter gender (M/F): ").upper()
        if gender in ["M", "F"]:
            break
        print("✗ Invalid input. Please enter 'M' or 'F'")

    while True:
        try:
            height = float(input("Enter height in cm (positive number): "))
            if height > 0:
                break
            print("✗ Height must be positive")
        except ValueError:
            print("✗ Invalid input. Please enter a number")

    Person(surname, gender, height)
    print("✓ Person added successfully\n")


def find_by_surname():
    print("\n" + "-" * 40)
    print("Find by Surname")
    print("-" * 40)

    surname = input_with_validator(
        "Enter surname to search: ",
        str.isalpha
    )

    person = Person.search_by_surname(surname)

    if person:
        print(f"\n✓ Found person:")
        print(person)
    else:
        print(f"✗ No person found with surname '{surname}'")

    print()


def find_by_letter():
    print("\n" + "-" * 40)
    print("Find by First Letter")
    print("-" * 40)

    letter = input_with_validator(
        "Enter the first letter of surname: ",
        str.isalpha
    )

    persons = Person.search_by_letter(letter)

    if persons:
        print(f"\n✓ Found {len(persons)} person(s):\n")
        for idx, person in enumerate(persons, 1):
            print(f"{idx}. {person}")
    else:
        print(f"✗ No persons found starting with '{letter}'")

    print()


def calculate_average_height_women():
    print("\n" + "-" * 40)
    print("Average Height of Women")
    print("-" * 40)

    average = Person.get_average_height_women()

    if average is not None:
        women = [p for p in Person.all_persons if p.gender == "F"]
        print(f"\n✓ Total women: {len(women)}")
        print(f"✓ Average height: {average:.2f} cm\n")
    else:
        print("\n✗ No women found in the database\n")


def find_tallest_man():
    print("\n" + "-" * 40)
    print("Tallest Man")
    print("-" * 40)

    man = Person.get_tallest_man()

    if man:
        print(f"\n✓ Tallest man:")
        print(f"   Surname: {man.last_name}")
        print(f"   Height: {man.height} cm\n")
    else:
        print("\n✗ No men found in the database\n")


def check_same_height():
    print("\n" + "-" * 40)
    print("Same Height Check")
    print("-" * 40)

    if Person.check_same_height_pair():
        print("\n✓ Yes, there are people with same height:\n")

        heights_dict = {}
        for person in Person.all_persons:
            if person.height not in heights_dict:
                heights_dict[person.height] = []
            heights_dict[person.height].append(person)

        # Display groups with 2+ people
        for height, people in sorted(heights_dict.items()):
            if len(people) > 1:
                print(f"Height {height} cm - {len(people)} people:")
                for person in people:
                    print(f"   • {person.last_name}")
        print()
    else:
        print("\n✗ No two people have the same height\n")


def display_person_info():
    print("\n" + "-" * 40)
    print("Display Person Information")
    print("-" * 40)

    surname = input_with_validator(
        "Enter surname to search: ",
        str.isalpha
    )

    person = Person.search_by_surname(surname)

    if person:
        print("\n" + "=" * 50)
        print("Person Information")
        print("=" * 50)
        print(f"Surname:  {person.last_name}")
        print(f"Gender:   {'Female' if person.gender == 'F' else 'Male'}")
        print(f"Height:   {person.height} cm")
        print("=" * 50 + "\n")
    else:
        print(f"\n✗ Person with surname '{surname}' not found\n")


def show_all_persons():
    Person.print_all(Person.all_persons)


def print_description():
    print(DESCRIPTION)


def task1():
    print_description()

    while True:
        display_menu()

        try:
            choice = input_data("Choose an option: ",  int, 0, 12)
            match choice:
                case 1:
                    add_person()
                case 2:
                    find_by_surname()
                case 3:
                    find_by_letter()
                case 4:
                    calculate_average_height_women()
                case 5:
                    find_tallest_man()
                case 6:
                    check_same_height()
                case 7:
                    display_person_info()
                case 8:
                    show_all_persons()
                case 9:
                    save_to_csv()
                case 10:
                    load_from_csv()
                case 11:
                    save_to_pickle()
                case 12:
                    load_from_pickle()
                case 0:
                    print("\n✓ Returning to main menu...\n")
                    break

        except KeyboardInterrupt:
            print("\n\n✓ Program interrupted by user")
            break
        except Exception as e:
            print(f"✗ An error occurred: {e}")
