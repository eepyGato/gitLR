# ---------------------------------------------------------
# Lab Work №4 - Task 5 (Variant 9)
# Module: task5.py
# Purpose: Main task logic for matrix operations
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

from task5.matrix_creator import MatrixCreator, MatrixAnalyzer
from utils.inputValidator import input_data

DESCRIPTION = r"""
╔═══════════════════════════════════════════════════════════╗
║                  NumPy Matrix Operations                  ║
║                                                           ║
║  Task: Working with integer matrices and statistics       ║
║                                                           ║
║  Main operations:                                         ║
║  • Generate random integer matrix A[n,m]                  ║
║  • Swap max elements in first and last columns            ║
║  • Calculate correlation coefficient                      ║
║  • Compute statistical measures                           ║
║                                                           ║
║  Statistical functions:                                   ║
║  • mean()     - Average value                             ║
║  • median()   - Middle value when sorted                  ║
║  • var()      - Variance (dispersion)                     ║
║  • std()      - Standard deviation                        ║
║  • corrcoef() - Correlation coefficient                   ║
╚═══════════════════════════════════════════════════════════╝
"""


def print_description():
    """Print task description."""
    print(DESCRIPTION)


def task5() -> bool:
    """
    Main function for matrix operations.

    Variant 9:
    1. Swap maximum elements in first and last columns
    2. Calculate correlation coefficient between columns
    3. Round result to 2 decimal places

    Returns:
        bool: Always True to return to menu
    """
    print_description()

    while True:
        print("\n" + "=" * 70)
        print("MATRIX PARAMETERS".center(70))
        print("=" * 70)

        try:
            rows = input_data(
                "\nEnter number of rows (n >= 2): ",
                int,
                min_value=2
            )

            cols = input_data(
                "Enter number of columns (m >= 2): ",
                int,
                min_value=2
            )

            print(f"\nGenerating {rows}x{cols} random integer matrix...")
            matrix_obj = MatrixCreator(rows, cols)
            matrix_obj.generate_matrix()
            matrix = matrix_obj.get_matrix()

            print("\n" + "-" * 70)
            print("GENERATED MATRIX:")
            print("-" * 70)
            print(matrix)

            # Get columns before swap
            first_col_before = matrix_obj.get_first_column().copy()
            last_col_before = matrix_obj.get_last_column().copy()

            print("\n" + "-" * 70)
            print("MAXIMUM ELEMENTS:")
            print("-" * 70)
            (max_first, idx_first), (max_last, idx_last) = matrix_obj.swap_max_elements()
            print(f"Max in first column: {max_first} at index [{idx_first}]")
            print(f"Max in last column:  {max_last} at index [{idx_last}]")

            print("\n" + "-" * 70)
            print("MATRIX AFTER SWAP:")
            print("-" * 70)
            print(matrix_obj.get_matrix())

            print("\n" + "-" * 70)
            print("CORRELATION ANALYSIS:")
            print("-" * 70)

            analyzer = MatrixAnalyzer(matrix)

            corr_original = analyzer.correlation_columns(
                first_col_before,
                last_col_before
            )
            print(f"Correlation (before swap): {corr_original}")

            first_col_after = matrix_obj.get_first_column()
            last_col_after = matrix_obj.get_last_column()
            corr_after = analyzer.correlation_columns(
                first_col_after,
                last_col_after
            )
            print(f"Correlation (after swap):  {corr_after}")

            print("\n" + "-" * 70)
            print("STATISTICAL MEASURES:")
            print("-" * 70)

            stats = analyzer.all_stats
            print(f"Mean:                  {stats['mean']:.4f}")
            print(f"Median:                {stats['median']:.4f}")
            print(f"Variance:              {stats['variance']:.4f}")
            print(f"Std Dev (built-in):    {stats['std_builtin']}")
            print(f"Std Dev (manual):      {stats['std_manual']}")

            min_val, min_indices = matrix_obj.find_min_elements()
            print("\n" + "-" * 70)
            print(f"Minimum value: {min_val}")
            print(f"Found at indices:\n{min_indices}")

        except ValueError as e:
            print(f"\n✗ Invalid input: {e}")
        except Exception as e:
            print(f"\n✗ Error: {e}")

        print("\n" + "-" * 70)
        again = input("Process another matrix? (1=yes, other=no): ").strip()

        if again != '1':
            print("\n✓ Returning to main menu...\n")
            return True
