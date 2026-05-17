# ---------------------------------------------------------
# Lab Work №4 - Task 6
# Module: task6.py
# Purpose: Pandas Series and DataFrame Analysis
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

import pandas as pd
from task6.pandas_analyzer import DataInfo, RatingPriceAnalyzer, QualityReviewsAnalyzer
from utils.inputValidator import input_data, input_with_validator

TASK_DESCRIPTION = r"""
========================================================================
                         Pandas Data Analysis
========================================================================

PART A: Pandas Series and DataFrame Basics
   1. Pandas library import and basic operations
   2. Series structure and creation
   3. Series element access using .loc and .iloc
   4. DataFrame object creation and structure
   5. DataFrame information display

PART B: Data Analysis Operations
   1. Get DataFrame information for each parameter
   2. Statistical methods for data indexing
   3. Calculate ratios:
      avg(target) at max(condition) / avg(target) at min(condition)

Example Dataset: Product Sales Data
   Columns: Product, Price, Rating, Reviews, Quality Score

========================================================================
"""


def print_task_description():
    """Print task description."""
    print(TASK_DESCRIPTION)


def part_a_demonstration():
    """Part A: Demonstrate Series and DataFrame basics."""
    print("\n" + "=" * 70)
    print("PART A: PANDAS BASICS")
    print("=" * 70)

    basics = DataInfo(None)
    basics.show_series()
    print()
    basics.show_dataframe()


def part_b_analysis():
    """Part B: Perform data analysis."""
    print("\n" + "=" * 70)
    print("PART B: PRODUCT DATA ANALYSIS")
    print("=" * 70 + "\n")

    filepath = input_with_validator(
        "Enter path to dataset CSV: ",
        lambda x: len(x) > 0 and x.endswith('.csv')
    )

    try:
        df = pd.read_csv(filepath)
        print(f"\nDataset loaded: {df.shape[0]} rows, {df.shape[1]} columns\n")

        info = DataInfo(df)
        info.dataframe_info()

        print("\n" + "=" * 70)
        print("ANALYSIS RESULTS")
        print("=" * 70)

        print("\nQuestion 1: Rating and Price Relationship")
        print("How many times higher is price for high-rated vs low-rated products?")
        ratio = RatingPriceAnalyzer(df).analyze_ratio()
        print(f"Answer: {ratio}x")

        print("\n" + "-" * 70)
        print("\nQuestion 2: Quality Score and Reviews Relationship")
        print("What is the difference in average reviews between")
        print("high and low quality products?")
        gap = QualityReviewsAnalyzer(df).analyze_gap()
        print(f"Answer: {gap} reviews")

        return df

    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def task6() -> bool:
    """
    Main task 6 function.

    Demonstrates:
    - Pandas Series and DataFrame creation
    - Data access methods (.loc, .iloc)
    - Statistical analysis operations
    - Real-world data analysis examples

    Returns:
        bool: Always True to return to menu
    """
    print_task_description()

    while True:
        print("\n" + "=" * 70)
        print("TASK 6 MENU")
        print("=" * 70)

        print("\n1. Part A: Series & DataFrame Basics")
        print("2. Part B: Product Data Analysis")
        print("3. Return to Main Menu")

        choice = input_data("Select option (1-3): ", int, min_value=1, max_value=3)
        choice = str(choice)

        if choice == '1':
            part_a_demonstration()

        elif choice == '2':
            part_b_analysis()

        elif choice == '3':
            print("\nReturning to main menu...\n")
            return True

        again = input_data("Continue? (1=yes, other=no): ", int, min_value=0, max_value=9)
        if again != 1:
            print("\nReturning to main menu...\n")
            return True

