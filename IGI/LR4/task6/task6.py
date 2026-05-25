# ---------------------------------------------------------
# Lab Work №4 - Task 6 (Variant 27 - Sberbank Housing)
# Module: task6.py
# Version: 1.0
# Developer: Shcherbak Rodion
# Date of Development: 2026-04-29
# ---------------------------------------------------------

import pandas as pd
import numpy as np
from task6.pandas_analyzer import PandasBasics, HousingAnalyzer
from utils.inputValidator import input_data, input_with_validator

DESCRIPTION = """
======================================================================
                     Task 6 - Variant 27 (Sberbank Housing)
======================================================================

PART A: Pandas Series and DataFrame Basics
   1. Import Pandas
   2. Series structure and creation
   3. Access with .loc and .iloc
   4. DataFrame creation

PART B: Housing Data Analysis
   1. Get DataFrame information
   2. Create sample of 5 random transactions (price, full_sq, floor)
   3. Reset index and save old index as column
   4. Calculate ratio: avg(price/full_sq) in richest vs poorest districts
======================================================================
"""


def load_housing_data():
    """Load Sberbank housing data or create test data"""
    import os
    
    paths = ['test_data.csv', 'housing_data.csv', 'sberbank_housing.csv']
    for path in paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                print(f"Loaded: {path} ({df.shape[0]} rows)")
                return df
            except:
                pass
    
    print("Creating test data...")
    np.random.seed(42)
    
    districts = {'Arbat': 2.5, 'Khamovniki': 2.4, 'Tverskoy': 2.3, 'Presnensky': 2.2,
                 'Yakimanka': 2.2, 'Zamoskvorechye': 1.9, 'Basmanny': 1.8, 'Meshchansky': 1.8,
                 'Tagansky': 1.7, 'Danilovsky': 1.4, 'Donskoy': 1.3, 'Lefortovo': 1.2,
                 'Begovoy': 1.2, 'Sokolniki': 1.0, 'MaryinaRoshcha': 0.9, 'Yuzhnoportovy': 0.7}
    
    data = []
    for _ in range(500):
        district = np.random.choice(list(districts.keys()))
        multiplier = districts[district]
        full_sq = np.random.uniform(25, 120)
        price = 150000 * multiplier * full_sq * np.random.uniform(0.7, 1.3)
        data.append({
            'price': int(price),
            'full_sq': round(full_sq, 1),
            'floor': np.random.randint(1, 26),
            'sub_area': district
        })
    
    return pd.DataFrame(data)


def task6():
    """Main function for Task 6"""
    print(DESCRIPTION)
    
    while True:
        print("\n" + "=" * 60)
        print("MENU")
        print("=" * 60)
        print("1. Part A: Series & DataFrame Basics")
        print("2. Part B: Housing Data Analysis")
        print("3. Return to Main Menu")
        
        choice = input_data("Choose option (1-3): ", int, 1, 3)
        
        if choice == 1:
            print("\n" + "=" * 40)
            print("PART A: PANDAS BASICS")
            print("=" * 40)
            PandasBasics.show_series()
            PandasBasics.show_dataframe()
            
        elif choice == 2:
            print("\n" + "=" * 40)
            print("PART B: HOUSING ANALYSIS")
            print("=" * 40)
            df = load_housing_data()
            analyzer = HousingAnalyzer(df)
            analyzer.run_all_tasks()
            
        elif choice == 3:
            print("\nReturning to main menu...")
            return True
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    task6()