Folder Audit Tool — V3
A Python utility for auditing folders, exporting file metadata, and safely identifying duplicate files without destructive actions.
This tool is designed for disk analysis, cleanup planning, and reporting, not automated deletion — making it suitable for
real-world use and portfolio demonstration.

Features
Core Audit
    Recursively or non-recursively scans a target folder
    Collects file metadata:
        Filename
        Full path
        Extension
        Size (KB)
        Last modified date
    Exports full results to CSV
    Console summary:
        Total files
        Total size
        Average file size
        Median file size

File Type Analysis
    Extension breakdown:
        File count per extension
        Total size per extension
Human-readable console output

Duplicate File Detection (V3 Highlight)
Safely identifies potential duplicates without deleting anything.

Two detection modes:
    By file size
        Matches files with the same size and extension
    By filename
        Matches files with the same filename regardless of extension

Duplicates are:
    Printed clearly to the console
    Exported to separate CSV files for review

Output Files
The tool generates the following CSV files:
    folder_audit.csv - Complete file audit
    duplicates_by_size.csv - Duplicates grouped by size + extension
    duplicates_by_name.csv - Duplicates grouped by filename

All CSV files are Excel-friendly.

Configuration
Edit these values in main():
    folder_to_scan = rC:\Insert_Folder_Path_Here"     # Folder to audit
    output_csv = "folder_audit.csv"

Optional behaviour flags:
    RECURSIVE = True       # Scan subfolders
    MIN_SIZE_KB = 10       # Ignore very small files
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

Usage
python folder_auditV3.py

Console output includes:
    Summary statistics
    File type breakdown
    Duplicate listings

CSV files are written to the script directory.

Safety Philosophy
This tool:
    Does not delete files
    Does not modify files
    Does not auto-resolve duplicates

All duplicate handling is manual and review-based via exported CSVs.

This design choice prioritizes safety and real-world usability.

Example Use Cases
    Hard drive cleanup planning
    Storage usage analysis
    Identifying duplicate documents/media
    Pre-migration audits
    Backup verification

Roadmap (V4 Ideas)
Planned future enhancements:
    SHA-256 content hashing (true duplicates)
    Optional file move/delete (explicit opt-in)
    Configurable output paths
    JSON export
    CLI arguments

Status
Version: V3
State: Frozen / Portfolio Ready
Python: 3.10+
Dependencies: Standard Library Only

Author
Built as part of a Python learning and portfolio development journey, focused on practical utilities, safe design, and real-world value.

Darren Williamson
Python Utility Development * Automation * Data Analysis
Uk Citizen / Spain-based / Remote
LinkedIn: https://www.linkedin.com/in/darren-williamson3/