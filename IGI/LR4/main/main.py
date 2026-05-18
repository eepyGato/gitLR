# ------------------------------------------------------------------------------------------
# Lab Work №4
# Topic: Standard Data Types, Collections, Functions, Modules,
#        Files, Classes, Serializers, Regular Expressions
# Goal: Master the basic syntax of Python, gain skills working with standard data types,
#       collections, functions, modules, files, classes, serializers, regular expressions
#       and reinforce them by developing interactive applications.
# Version: 1.0
# Developer: Shcherbak Rodion
# Date of Development: 2026-04-29
# ------------------------------------------------------------------------------------------

from task1.task1 import task1
from task2.task2 import task2
from task3.task3 import task3
from task4.task4 import task4
from task5.task5 import task5
from task6.task6 import task6

from utils.inputValidator import input_data

def run_task1():
    """Execute Task 1"""
    task1()


def run_task2():
    """Execute Task 2"""
    task2()


def run_task3():
    """Execute Task 3"""
    task3()


def run_task4():
    """Execute Task 4"""
    task4()


def run_task5():
    """Execute Task 5"""
    task5()


def run_task6():
    """Execute Task 6"""
    task6()


def main() -> None:
    """
    Main function to run the program.

    Displays menu and executes selected tasks.
    """
    while True:
        print("\n" + "=" * 60)
        print("Laboratory Work №4 - Menu")
        print("=" * 60)
        print("1. Task 1: Personal Data Management System")
        print("2. Task 2: Text Analysis System")
        print("3. Task 3: Arcsin Series Expansion Calculator")
        print("4. Task 4: Regular Polygon Constructor")
        print("5. Task 5: NumPy Matrix Operations")
        print("6. Task 6: Pandas Data Analysis")
        print("0. Exit")
        print("=" * 60)

        select = input_data("Input number of task: ", int, 0, 6)

        match select:
            case 1:
                run_task1()
            case 2:
                run_task2()
            case 3:
                run_task3()
            case 4:
                run_task4()
            case 5:
                run_task5()
            case 6:
                run_task6()
            case 0:
                print("\n✓ Exiting program. Goodbye!")
                break


if __name__ == "__main__":
    main()
