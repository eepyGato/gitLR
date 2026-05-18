# ---------------------------------------------------------
# Lab Work №4 - Task 3 (Variant 9)
# Module: task3.py
# Purpose: Calculate arccos(x) using series expansion
# Version: 1.1 (IMPROVED)
# Developer: Developer: Shcherbak Rodion
# Date of Development: 2026-04-29
# ---------------------------------------------------------

from tabulate import tabulate
from task3.series import ArcsinSeries
from task3.plot import plot_series_vs_math
from utils.inputValidator import input_data

DESCRIPTION = r"""
╔═══════════════════════════════════════════════════════════╗
║             Arcsin Series Expansion Calculator            ║
║                                                           ║
║  Formula: arcsin(x) = π/2 - arcsin(x) =                   ║
║  π/2 - Σ [(2n)! / (4^n * (n!)^2 * (2n+1))] * x^(2n+1)     ║  
║                                                           ║
║  Valid for: |x| ≤ 1                                       ║
║                                                           ║
║  This program:                                            ║
║  • Calculates arcsin(x) using series expansion            ║
║  • Compares with math.acos() result                       ║
║  • Computes statistical measures                          ║
║  • Plots comparison graph                                 ║
║  • Saves results to file                                  ║
╚═══════════════════════════════════════════════════════════╝
"""


def print_description():
    """Print task description."""
    print(DESCRIPTION)


def display_results(x_val, n, fx, math_fx, eps, stats):
    """
    Display calculation results in formatted tables.

    Args:
        x_val (float): Argument value
        n (int): Number of terms used
        fx (float): Series approximation result
        math_fx (float): Math module result
        eps (float): Precision used
        stats (dict): Statistical measures
    """
    print("\n" + "=" * 70)
    print("CALCULATION RESULTS".center(70))
    print("=" * 70)

    error = abs(fx - math_fx)
    rel_error = (error / abs(math_fx) * 100) if math_fx != 0 else 0

    print("\n--- Main Results ---")
    results_table = [
        [x_val, n, fx, math_fx, eps, error]
    ]
    print(tabulate(
        results_table,
        headers=["x", "n", "F(x)", "arcsin(x)", "eps", "Error"],
        tablefmt="grid",
        floatfmt=".10f"
    ))

    print("\n--- Statistical Measures of Series Terms ---")
    mode_val = stats["Mode"]
    if isinstance(mode_val, float):
        mode_str = f"{mode_val:.10f}"
    else:
        mode_str = str(mode_val)

    stats_table = [
        ["Mean", f"{stats['Mean']:.10f}"],
        ["Median", f"{stats['Median']:.10f}"],
        ["Mode", mode_str],
        ["Variance", f"{stats['Variance']:.10f}"],
        ["Standard Deviation", f"{stats['Stdev']:.10f}"]
    ]
    print(tabulate(
        stats_table,
        headers=["Measure", "Value"],
        tablefmt="grid"
    ))

    print(f"\n{'=' * 70}")
    print(f"✓ Convergence achieved in {n} iterations")
    print(f"✓ Absolute error: {error:.2e}")
    print(f"✓ Relative error: {rel_error:.6f}%")

    if error < 1e-10:
        print("✓ EXCELLENT convergence!")
    elif error < 1e-6:
        print("✓ VERY GOOD convergence!")
    elif error < 1e-3:
        print("✓ GOOD convergence!")
    else:
        print("Warning: Error is large. Consider smaller epsilon.")


def task3():
    """
    Main function for arcsin series calculator.

    Handles user input, calculations, statistics, and plotting.

    Returns:
        None (Returns to main menu)
    """
    print_description()

    while True:
        print("\n" + "-" * 70)
        print("Input Parameters".center(70))
        print("-" * 70)

        try:
            x = input_data(
                "Enter x (|x| ≤ 1): ",
                float,
                min_value=-1,
                max_value=1
            )

            eps = input_data(
                "Enter epsilon (0 < eps < 1): ",
                float,
                min_value=0,
                max_value=1
            )

            if eps > 0.1:
                print("\n Warning: Large epsilon may result in few iterations.")
                print("   Recommended: ε < 0.1 for better statistics")

            if abs(x) >= 0.99:
                print("\n Warning: x ≥ ±0.99 is near boundary.")
                print("   The series converges VERY SLOWLY at boundaries.")
                print("   For better results, use smaller epsilon (< 1e-6)")

            if abs(x) < 1e-10:
                print("\n✓ Note: For x ≈ 0, arcsin(x) ≈ π/2 ≈ 1.5708")

            print("\nCalculating arcsin series expansion...")

            calc = ArcsinSeries(x, eps)
            calc.calculate()

            x_val, n, fx, math_fx, eps_val = calc.get_results()
            stats = calc.get_statistics()

            display_results(x_val, n, fx, math_fx, eps_val, stats)

            print("\nGenerating plot...")
            plot_series_vs_math(calc.terms, math_fx, x)

        except ValueError as e:
            print(f"✗ Invalid input: {e}")
        except Exception as e:
            print(f"✗ Error: {e}")

        print("\n" + "-" * 70)
        again = input("Press '1' to calculate again or any other key to exit: ").strip()

        if again != '1':
            print("\n✓ Returning to main menu...\n")
            break
