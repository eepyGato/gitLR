# ---------------------------------------------------------
# Lab Work №4 - Task 4 (Variant 9)
# Module: plot.py
# Purpose: Visualization of geometric figures
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

import os
import math
import matplotlib.pyplot as plt
from datetime import datetime


def get_path_to_file(file: str) -> str:
    """Get the path to save files."""
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    files_dir = os.path.join(current_file_dir, 'files')

    os.makedirs(files_dir, exist_ok=True)

    return os.path.join(files_dir, file)


def draw_polygon(polygon):
    """Draw and display regular polygon using matplotlib."""
    n = polygon.n_sides
    a = polygon.side_length
    color = polygon.color
    label = polygon.label

    circumradius = polygon.get_circumradius()

    vertices = []
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2  # Start from top
        x = circumradius * math.cos(angle)
        y = circumradius * math.sin(angle)
        vertices.append((x, y))

    vertices.append(vertices[0])

    x_coords = [v[0] for v in vertices]
    y_coords = [v[1] for v in vertices]

    plt.figure(figsize=(10, 10))
    plt.plot(x_coords, y_coords, color=color, linewidth=2, label=f'{polygon.get_name()}')
    plt.fill(x_coords, y_coords, color=color, alpha=0.4)
    plt.scatter(x_coords[:-1], y_coords[:-1], color='red', s=50, zorder=5)
    plt.scatter(0, 0, color='black', s=100, marker='x', zorder=5)
    plt.title(label if label else f'{polygon.get_name()} (n={n}, a={a:.2f})', fontsize=14, fontweight='bold')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.legend()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"polygon_{n}_{timestamp}.png"
    filepath = get_path_to_file(filename)

    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    print(f"\n✓ Plot saved to: {filepath}")

    plt.show()


def draw_rectangle(rectangle):
    """Draw and display rectangle using matplotlib."""
    width = rectangle.width
    height = rectangle.height
    color = rectangle.color
    label = rectangle.label

    x_half = width / 2
    y_half = height / 2

    vertices = [
        (-x_half, -y_half),
        (x_half, -y_half),
        (x_half, y_half),
        (-x_half, y_half),
        (-x_half, -y_half)
    ]

    x_coords = [v[0] for v in vertices]
    y_coords = [v[1] for v in vertices]

    plt.figure(figsize=(10, 8))
    plt.plot(x_coords, y_coords, color=color, linewidth=2, label=f'{rectangle.get_name()}')
    plt.fill(x_coords, y_coords, color=color, alpha=0.4)
    plt.scatter(x_coords[:-1], y_coords[:-1], color='red', s=50, zorder=5)
    plt.scatter(0, 0, color='black', s=100, marker='x', zorder=5)
    plt.title(label if label else f'{rectangle.get_name()} ({width:.2f}x{height:.2f})',
              fontsize=14, fontweight='bold')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.legend()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"rectangle_{timestamp}.png"
    filepath = get_path_to_file(filename)

    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    print(f"\n✓ Plot saved to: {filepath}")

    plt.show()
