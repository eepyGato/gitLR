# ---------------------------------------------------------
# Lab Work №4 - Task 3 (Variant 9)
# Module: plot.py
# Purpose: Plotting utilities for series visualization
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

import os
import matplotlib.pyplot as plt
from matplotlib import ticker
from datetime import datetime

plt.rcParams['text.usetex'] = False
plt.rcParams['font.family'] = 'DejaVu Sans'


def get_path_to_file(file: str) -> str:
    """
    Get absolute path to file in task3/files directory.

    Args:
        file (str): Filename

    Returns:
        str: Absolute path to file
    """
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    files_dir = os.path.join(current_file_dir, 'files')

    os.makedirs(files_dir, exist_ok=True)

    return os.path.join(files_dir, file)


def plot_series_vs_math(fx_values: list, math_fx: float, x: float):
    """
    Plot series approximation vs actual math function.

    Creates a comparison graph with:
    - Blue line with markers: Series approximation values
    - Red dashed line: Actual math function value
    - Annotated points
    - Grid and axes

    Args:
        fx_values (list): Accumulated function values at each iteration
        math_fx (float): Actual arcsin(x) value from math module
        x (float): Argument value used in calculation
    """
    n_values = list(range(1, len(fx_values) + 1))
    math_fx_line = [math_fx for _ in n_values]

    fig, ax = plt.subplots(figsize=(13, 8))

    ax.plot(
        n_values,
        fx_values,
        label=f"Series Approximation (x={x:.4f})",
        color="blue",
        marker='o',
        linewidth=2.5,
        markersize=7,
        alpha=0.75,
        markerfacecolor='lightblue',
        markeredgewidth=2
    )

    ax.plot(
        n_values,
        math_fx_line,
        label=f"Exact arcsin({x:.4f})",
        color="red",
        linestyle="--",
        linewidth=3,
        alpha=0.85,
        marker='s',
        markersize=6,
        markerfacecolor='mistyrose'
    )

    title = "Arcsin Series Approximation vs Math Function"
    ax.set_title(
        title,
        fontsize=14,
        fontweight='bold',
        pad=20
    )

    ax.set_xlabel("Number of Terms (n)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Function Value F(x)", fontsize=12, fontweight='bold')

    ax.legend(
        fontsize=11,
        loc='best',
        framealpha=0.95,
        shadow=True,
        fancybox=True,
        edgecolor='black',
        frameon=True
    )

    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)

    ax.axhline(0, color='black', linewidth=0.8, alpha=0.5)
    ax.axvline(0, color='black', linewidth=0.8, alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.4f'))

    last_term_value = fx_values[-1]
    last_n = n_values[-1]

    if len(n_values) > 1:
        offset_n = max(1, last_n // 4)
        offset_y = (max(fx_values) - min(fx_values)) * 0.15 if len(set(fx_values)) > 1 else 0.1
    else:
        offset_n = 1
        offset_y = 0.1

    ax.annotate(
        f"Final: F(x) = {last_term_value:.8f}",
        xy=(last_n, last_term_value),
        xytext=(last_n - offset_n, last_term_value + offset_y),
        arrowprops=dict(
            arrowstyle='->',
            connectionstyle='arc3,rad=0.3',
            color='blue',
            lw=2.5
        ),
        fontsize=10,
        bbox=dict(
            boxstyle='round,pad=0.8',
            facecolor='yellow',
            alpha=0.85,
            edgecolor='darkorange',
            linewidth=2
        ),
        ha='center',
        fontweight='bold'
    )

    ax.annotate(
        f"Exact: arcsin({x:.4f}) = {math_fx:.8f}",
        xy=(last_n, math_fx),
        xytext=(last_n - offset_n, math_fx - offset_y),
        arrowprops=dict(
            arrowstyle='->',
            connectionstyle='arc3,rad=-0.3',
            color='red',
            lw=2.5
        ),
        fontsize=10,
        bbox=dict(
            boxstyle='round,pad=0.8',
            facecolor='lightcyan',
            alpha=0.85,
            edgecolor='darkred',
            linewidth=2
        ),
        ha='center',
        fontweight='bold'
    )

    error = abs(last_term_value - math_fx)
    relative_error = (error / abs(math_fx) * 100) if math_fx != 0 else 0

    info_text = (
        f"Absolute Error: {error:.2e}\n"
        f"Relative Error: {relative_error:.6f}%\n"
        f"Terms Used: {len(n_values)}"
    )
    ax.text(
        0.02, 0.98,
        info_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='top',
        bbox=dict(
            boxstyle='round,pad=0.9',
            facecolor='lightyellow',
            alpha=0.92,
            edgecolor='black',
            linewidth=1.5
        ),
        fontweight='bold',
        family='monospace'
    )

    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"arcsin_plot_{timestamp}.png"
    filepath = get_path_to_file(filename)

    try:
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"\n✓ Plot saved to: {filepath}")
    except Exception as e:
        print(f"\n✗ Error saving plot: {e}")

    plt.show()
