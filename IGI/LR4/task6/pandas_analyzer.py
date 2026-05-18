# ---------------------------------------------------------
# Lab Work №4 - Task 6 (Variant 27 - Sberbank Housing)
# Module: pandas_analyzer.py
# Version: 1.0
# Developer: Shcherbak Rodion
# Date of Development: 2026-04-29
# ---------------------------------------------------------

import pandas as pd
import numpy as np
from IPython.display import display


class PandasBasics:
    """Demonstrates basic Pandas Series and DataFrame operations"""

    @staticmethod
    def show_series():
        series = pd.Series([100, 200, 300], index=['x', 'y', 'z'])
        print("Series content:")
        display(series)
        print(f"Access by .loc['y']: {series.loc['y']}")
        print(f"Access by .iloc[1]: {series.iloc[1]}")

    @staticmethod
    def show_dataframe():
        df = pd.DataFrame({
            "price": [7500000, 5200000, 8900000],
            "full_sq": [65, 42, 78],
            "floor": [5, 3, 12],
            "sub_area": ["Arbat", "Presnensky", "Khamovniki"]
        })
        print("DataFrame content:")
        display(df)


class HousingAnalyzer:
    """Housing data analysis for Variant 27"""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def dataframe_info(self):
        """Get DataFrame information for each parameter"""
        print("\nDataFrame Info:")
        print(f"Shape: {self.df.shape}")
        print(f"Columns: {list(self.df.columns)}")
        print("\nData types:")
        print(self.df.dtypes)
        print("\nStatistics:")
        display(self.df.describe())
        print("\nFirst 5 rows:")
        display(self.df.head())

    def task1_create_sample(self, n=5):
        """Create DataFrame from n random transactions (price, full_sq, floor)"""
        sample = self.df.sample(n=n, random_state=42)
        return sample[['price', 'full_sq', 'floor']].copy()

    def task2_reset_index_with_save(self, df):
        """Reset index and save old index as separate column"""
        result = df.reset_index()
        result = result.rename(columns={'index': 'old_index'})
        return result

    def task3_price_per_sqm_ratio(self):
        """Calculate ratio: avg(price/full_sq) in richest vs poorest districts"""
        self.df['price_per_sqm'] = self.df['price'] / self.df['full_sq']
        district_avg = self.df.groupby('sub_area')['price_per_sqm'].mean()
        ratio = district_avg.max() / district_avg.min()
        return round(ratio, 2)

    def run_all_tasks(self):
        """Execute all variant 27 tasks"""
        print("\n" + "=" * 60)
        print("VARIANT 27 - SBERBANK HOUSING ANALYSIS")
        print("=" * 60)
        
        self.dataframe_info()
        
        print("\n" + "-" * 40)
        print("TASK 1: Random sample (5 transactions)")
        sample = self.task1_create_sample(5)
        display(sample)
        
        print("\n" + "-" * 40)
        print("TASK 2: Reset index with save")
        reset_df = self.task2_reset_index_with_save(sample)
        display(reset_df)
        
        print("\n" + "-" * 40)
        print("TASK 3: Price per sqm ratio")
        ratio = self.task3_price_per_sqm_ratio()
        print(f"Richest district / Poorest district = {ratio}")
        
        return ratio