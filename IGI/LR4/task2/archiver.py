# ---------------------------------------------------------
# Lab Work №4 - Task 2 (Variant 9)
# Module: archiver.py
# Purpose: Archive results and manage ZIP files
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

import os
import zipfile


def ensure_directory_exists():
    """Create files directory if it doesn't exist."""
    file_path = get_path_to_file()
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)


def archive_file(filename: str) -> dict:
    """
    Archive result file to ZIP.

    Args:
        filename (str): Path to file to archive

    Returns:
        dict: Archive information
            - filename: name of file in archive
            - size: original file size in bytes
            - compress_size: compressed size in bytes
            - compression_ratio: compression percentage
    """
    ensure_directory_exists()
    zip_name = get_path_to_file()

    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
            zip_archive.write(filename, arcname=os.path.basename(filename))

        with zipfile.ZipFile(zip_name, 'r') as zip_archive:
            info = zip_archive.getinfo(os.path.basename(filename))

            compression_ratio = (
                (1 - info.compress_size / info.file_size) * 100
                if info.file_size > 0 else 0
            )

            return {
                "filename": info.filename,
                "size": info.file_size,
                "compress_size": info.compress_size,
                "compression_ratio": round(compression_ratio, 2)
            }

    except FileNotFoundError:
        print(f"✗ File not found: {filename}")
        return None
    except zipfile.BadZipFile:
        print("✗ Error creating ZIP file")
        return None


def save_results_to_file(filename: str, results: list):
    """
    Save analysis results to text file.

    Args:
        filename (str): Path to output file
        results (list): List of result strings
    """
    ensure_directory_exists()

    try:
        with open(filename, "w", encoding='utf-8') as file:
            for result in results:
                file.write(f"{result}\n\n")
        print(f"✓ Results saved to: {filename}")
    except IOError as e:
        print(f"✗ Error saving results: {e}")


def get_path_to_file() -> str:
    """
    Get absolute path to ZIP file.

    Returns:
        str: Path to result.zip
    """
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_file_dir, 'files', 'result.zip')
