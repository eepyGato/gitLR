# ---------------------------------------------------------
# Lab Work №4 - Task 5 (Variant 26)
# Module: task5.py
# Purpose: Main task logic for matrix operations
# Version: 1.0
# Developer: Shcherbak Rodion
# Date of Development: 2026-04-29
# ---------------------------------------------------------

from task5.matrix_creator import MatrixCreator, MatrixAnalyzer

DESCRIPTION = r"""
╔══════════════════════════════════════════════════════════════════════╗
║                  NumPy Matrix Operations (Variant 26)                 ║
║                                                                       ║
║  Task: Working with integer matrices and statistics                   ║
║                                                                       ║
║  Main operations:                                                     ║
║  • Generate random integer matrix A[n,m]                              ║
║  • Find first occurrence of minimum element                           ║
║  • Insert first row after the row containing the minimum element      ║
║  • Calculate median of the first row (two ways: built-in and manual)  ║
║                                                                       ║
║  Statistical functions:                                               ║
║  • mean()     - Average value                                         ║
║  • median()   - Middle value when sorted (NumPy built-in)             ║
║  • median()   - Middle value (manual calculation)                     ║
║  • corrcoef() - Correlation coefficient between rows                  ║
║  • var()      - Variance (dispersion)                                 ║
║  • std()      - Standard deviation                                    ║
╚══════════════════════════════════════════════════════════════════════╝
"""


def print_description():
    """Print task description."""
    print(DESCRIPTION)


def input_data(prompt: str, data_type, min_value=None, max_value=None):
    """
    Get validated input from user.

    Args:
        prompt (str): Input prompt
        data_type: Type to convert to (float or int)
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        Converted and validated value
    """
    while True:
        try:
            value = input(prompt)
            value = data_type(value)
            
            if min_value is not None and value < min_value:
                print(f"✗ Value must be >= {min_value}")
                continue
            if max_value is not None and value > max_value:
                print(f"✗ Value must be <= {max_value}")
                continue
            
            return value
        except ValueError:
            print(f"✗ Invalid input. Please enter a valid {data_type.__name__}")


def print_matrix(matrix, title="MATRIX"):
    """Print matrix with formatted output."""
    print("\n" + "-" * 70)
    print(title.center(70))
    print("-" * 70)
    print(matrix)
    print()


def task5() -> bool:
    """
    Main function for matrix operations.

    Variant 26:
    1. Insert first row after the row containing the first minimum element
    2. Calculate median of the first row (two ways: built-in and manual)

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
                "Enter number of columns (m >= 1): ",
                int,
                min_value=1
            )

            print(f"\nGenerating {rows}x{cols} random integer matrix...")
            matrix_obj = MatrixCreator(rows, cols)
            matrix_obj.generate_matrix()
            matrix = matrix_obj.get_matrix()
            
            print_matrix(matrix, "GENERATED MATRIX")

            # Find first minimum element
            print("\n" + "-" * 70)
            print("FINDING MINIMUM ELEMENT".center(70))
            print("-" * 70)
            
            min_row, min_col = matrix_obj.find_first_min_element()
            min_value = matrix_obj.min_value
            
            print(f"Minimum value: {min_value}")
            print(f"First occurrence at position: row {min_row}, column {min_col}")
            print(f"All occurrences of minimum value:")
            for idx in matrix_obj.min_indices:
                print(f"  • row {idx[0]}, column {idx[1]}")

            # Insert first row after the row with minimum element
            print("\n" + "-" * 70)
            print("INSERTING FIRST ROW".center(70))
            print("-" * 70)
            
            inserted_pos, min_row_pos = matrix_obj.insert_row_after_min()
            print(f"First row inserted at position: row {inserted_pos}")
            print(f"(after the row containing the first minimum at row {min_row_pos})")
            
            print_matrix(matrix_obj.get_matrix(), "MATRIX AFTER INSERTION")

            # Calculate median of the first row
            print("\n" + "-" * 70)
            print("MEDIAN OF THE FIRST ROW".center(70))
            print("-" * 70)
            
            first_row = matrix_obj.get_first_row()
            print(f"First row values: {first_row}")
            
            analyzer = MatrixAnalyzer(matrix_obj.get_matrix())
            
            median_builtin = analyzer.median_builtin(0)
            median_manual = analyzer.median_manual(0)
            
            print(f"\nMedian (NumPy built-in):   {median_builtin}")
            print(f"Median (manual calculation): {median_manual}")
            
            # Verify both methods give the same result
            if abs(median_builtin - median_manual) < 0.0001:
                print("✓ Both methods match!")
            else:
                print("⚠ Warning: Methods returned different results!")

            # Additional statistics for the first row
            print("\n" + "-" * 70)
            print("ADDITIONAL STATISTICS (First Row)".center(70))
            print("-" * 70)
            
            stats = analyzer.get_row_stats(0)
            print(f"Mean:                    {stats['mean']}")
            print(f"Variance:                {stats['variance']}")
            print(f"Standard Deviation:      {stats['std']}")

            # Correlation between first row and other rows
            print("\n" + "-" * 70)
            print("CORRELATION ANALYSIS".center(70))
            print("-" * 70)
            
            new_rows = matrix_obj.get_matrix().shape[0]
            for i in range(1, min(4, new_rows)):  # Show correlation with up to 3 rows
                corr = analyzer.correlation(0, i)
                print(f"Correlation (row 0 vs row {i}): {corr}")

            # Display final matrix info
            print("\n" + "-" * 70)
            print("FINAL MATRIX INFO".center(70))
            print("-" * 70)
            
            info = matrix_obj.get_matrix_info()
            print(f"Matrix shape: {info['shape']}")
            print(f"Total elements: {info['size']}")
            print(f"Minimum value in original matrix: {info['min_value']}")

        except ValueError as e:
            print(f"\n✗ Invalid input: {e}")
        except Exception as e:
            print(f"\n✗ Error: {e}")

        print("\n" + "-" * 70)
        again = input("Process another matrix? (1=yes, other=no): ").strip()

        if again != '1':
            print("\n✓ Returning to main menu...\n")
            return True


if __name__ == "__main__":
    task5()