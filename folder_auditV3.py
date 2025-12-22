"""
Folder Audit & Report Tool

Scans a folder (recursively) and generates a CSV report
containing metadata about each file

Author: Darren Williamson
"""

import os
import csv
import statistics
from datetime import datetime
from collections import defaultdict

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

MIN_SIZE_KB = 10  # Ignore files smaller thank this (KB)

RECURSIVE = True  # Set this to False if you only want to the top level folder

def scan_folder(folder_path):
    """
    Recursively scan a folder and return a list of file metadata dictionaries.
    """
    records = []

    for root, dirs, files in os.walk(folder_path):
        if not RECURSIVE and root != folder_path:
            continue
        for filename in files:
            full_path = os.path.join(root, filename)

            extension = os.path.splitext(filename)[1].lower()

            try:
                size_bytes = os.path.getsize(full_path)
                size_kb = round(size_bytes / 1024, 2)
                if size_kb < MIN_SIZE_KB:
                    continue

                modified_ts = os.path.getmtime(full_path)
                last_modified = datetime.fromtimestamp(modified_ts).strftime(DATE_FORMAT)

                record = {
                    "filename": filename,
                    "full_path": full_path,
                    "extension": extension,
                    "size_kb": size_kb,             # Float, not string
                    "last_modified": last_modified
                }

                records.append(record)

            except (PermissionError, FileNotFoundError):
                # Skip files we cannot access
                continue

    return records

def print_extensions_breakdown(records):
    extension_counts = defaultdict(int)
    extension_sizes = defaultdict(float)

    for r in records:
        ext = r["extension"].lower() if r["extension"] else "(no extension)"
        extension_counts[ext] += 1
        extension_sizes[ext] += r["size_kb"]

    print("\nFile type breakdown:")
    print("---------------------")

    for ext in sorted(extension_counts):
        count = extension_counts[ext]
        size_mb = extension_sizes[ext] / 1024
        print(f"{ext:10} | {count:4} files | {size_mb:8.2f} MB")

def find_duplicates(records, mode="size"):
    """
    Find potential duplicate files

    modes:
        "size" -> sames size AND same extension
        "name" -> same filename (extension ignored)
        """
    groups = defaultdict(list)

    for r in records:
        if mode == "size":
            key = (
                round(r["size_kb"] / 2),
                r["extension"].lower()
            )

        elif mode == "name":
            key = r["filename"].lower()

        else:
            raise ValueError("Mode must be either 'size' or 'name'")

        groups[key].append(r)

    # Only keep groups with duplicates
    return {k: v for k, v in groups.items() if len(v) > 1}

def print_duplicates(duplicates, mode):
    if not duplicates:
        print("No duplicates found by {mode}.")
        return

    print(f"Duplicate files by {mode}:")
    print("-" * 40)

    for key, files in duplicates.items():
        print(f"\nMatch: {key}(")
        for f in files:
            print(f"  - {f['full_path']} ({f['size_kb']:2f} KB")

def print_summary(records):
    total_files = len(records)
    total_size_kb = sum([r["size_kb"] for r in records])

    size_values = [r["size_kb"] for r in records if r["size_kb"] > 0]

    if size_values:
        median_size_kb = statistics.median(size_values)
    else:
        median_size_kb = 0

    if total_files > 0:
        average_size_kb = total_size_kb / total_files
    else:
        average_size_kb = 0

    print("\nSummary:")
    print("-------")
    print(f"Files included: {total_files}")
    print(f"Total size: {total_size_kb:.2f} KB")
    print(f"Average file size: {average_size_kb:.2f} KB")
    print(f"Median file size: {median_size_kb:.2f} KB")


def write_csv(records, output_csv):
    """
    Write file records to a CSV file.
    """

    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Header
        writer.writerow([
            "Filename",
            "Full Path",
            "Extension",
            "Size (KB)",
            "Last Modified"
        ])

        # Rows
        for r in records:
            writer.writerow([
                r["filename"],
                r["full_path"],
                r["extension"],
                f"{r['size_kb']:.2F}",   # Formatting happens here only
                r["last_modified"]
            ])

def write_duplicates_csv(duplicates, output_csv):
    """
    Write duplicate files to a CSV.
    Each row represents one file, grouped by a duplicate key 
    """
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Header
        writer.writerow([
            "Duplicate Group",
            "Filename",
            "Full_Path",
            "Extension",
            "Size (KB)",
            "Last Modified"
        ])

        for group_key, files in duplicates.items():
            for r in files:
                writer.writerow([
                    group_key,
                    r["filename"],
                    r["full_path"],
                    r["extension"],
                    f"{r['size_kb']:.2F}",
                    r["last_modified"]
                ])



def main():
    folder_to_scan = r"C:\Insert_Folder_Path_Here"   # 👈 change if needed
    output_csv = "folder_audit.csv"

    print("Starting folder audit...")

    records = scan_folder(folder_to_scan)

    print_summary(records)
    print_extensions_breakdown(records)

    dupes_by_size = find_duplicates(records, mode="size")
    print_duplicates(dupes_by_size, "name + size + extension")
    write_duplicates_csv(dupes_by_size, "duplicates by size.csv")

    dupes_by_name = find_duplicates(records, mode="name")
    print_duplicates(dupes_by_name, "name + size + extension")
    write_duplicates_csv(dupes_by_name, "duplicates by name.csv")

    print(f"Scan complete.")
    print(f"Files found: {len(records)}")
    print(f"CSV written to: {output_csv}")


if __name__ == "__main__":
    main()