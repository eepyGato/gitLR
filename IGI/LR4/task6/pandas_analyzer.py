# ---------------------------------------------------------
# Lab Work №4 - Task 6
# Module: pandas_analyzer.py
# Purpose: Pandas Series and DataFrame Analysis Classes
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

import pandas as pd
from IPython.display import display


class PandasBasics:
    """Demonstrates basic Pandas Series and DataFrame operations"""

    @staticmethod
    def show_series():
        """Creates and displays a Series with custom index"""
        series = pd.Series([100, 200, 300], index=['x', 'y', 'z'])
        print("Series content:")
        display(series)
        print(f"Access by .loc['y']: {series.loc['y']}")
        print(f"Access by .iloc[1]: {series.iloc[1]}")

    @staticmethod
    def show_dataframe():
        """Creates and displays a simple DataFrame"""
        df = pd.DataFrame({
            "Product": ["Laptop", "Phone", "Tablet"],
            "Price": [1000, 500, 300]
        })
        print("DataFrame content:")
        display(df)


class DataInfo(PandasBasics):
    """Extends PandasBasics to provide DataFrame information"""

    def __init__(self, df: pd.DataFrame):
        """Initialize with a DataFrame"""
        self.df = df

    def dataframe_info(self):
        """Displays detailed information about the DataFrame"""
        print("DataFrame Information:")
        self.df.info()


class BaseAnalyzer:
    """Base class for data analysis operations"""

    def __init__(self, df: pd.DataFrame):
        """Initialize with a DataFrame copy"""
        self.df = df.copy()

    def preprocess(self, numeric_cols):
        """Convert columns to numeric and remove invalid rows"""
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        self.df.dropna(subset=numeric_cols, inplace=True)

    def get_average_by_condition(self, condition_col, target_col, condition='max'):
        """Calculate average of target column for extreme value in condition column"""
        extreme_value = self.df[condition_col].max() if condition == 'max' else self.df[condition_col].min()
        return self.df[self.df[condition_col] == extreme_value][target_col].mean()

    def get_ratio(self, condition_col, target_col, numeric_cols):
        """Calculate ratio between max and min condition averages"""
        self.preprocess(numeric_cols)
        max_avg = self.get_average_by_condition(condition_col, target_col, 'max')
        min_avg = self.get_average_by_condition(condition_col, target_col, 'min')
        return round(max_avg / min_avg if min_avg != 0 else float('inf'), 2)


class RatingPriceAnalyzer(BaseAnalyzer):
    """Analyzes relationship between Rating and Price"""

    def analyze_ratio(self):
        """Calculate price ratio between highest and lowest rated products"""
        self.preprocess(['Rating', 'Price'])
        max_rating_idx = self.df['Rating'].idxmax()
        min_rating_idx = self.df['Rating'].idxmin()
        max_rating_price = self.df.loc[max_rating_idx, 'Price']
        min_rating_price = self.df.loc[min_rating_idx, 'Price']
        ratio = round(max_rating_price / min_rating_price, 2)
        return ratio


class QualityReviewsAnalyzer(BaseAnalyzer):
    """Analyzes relationship between Quality Score and Reviews"""

    def analyze_gap(self):
        """Calculate review count gap between highest and lowest quality products"""
        self.preprocess(['Quality_Score', 'Reviews'])
        max_quality_idx = self.df['Quality_Score'].idxmax()
        min_quality_idx = self.df['Quality_Score'].idxmin()
        max_quality_reviews = self.df.loc[max_quality_idx, 'Reviews']
        min_quality_reviews = self.df.loc[min_quality_idx, 'Reviews']
        gap = round(max_quality_reviews - min_quality_reviews, 2)
        return gap
