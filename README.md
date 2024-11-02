# Database-Normalizer
Database Normalization

# Database Normalization Tool

## Overview

The **Database Normalization Tool** is a Python-based application designed to normalize relational database schemas up to the 5th normal form. It decomposes tables based on functional dependencies (FDs) and multivalued dependencies (MVDs), minimizing redundancy and ensuring data consistency. This tool is ideal for database architects and developers looking to optimize their database design.

## Features

- **Automated Normalization**: Normalizes database schemas up to 5NF.
- **Dependency Parsing**: Reads functional and multivalued dependencies from input files.
- **Excel Integration**: Loads tables, attributes, and primary keys from Excel files.
- **Configurable Output**: Excludes foreign keys from output and retains primary keys as per user preferences.
- **Built-in Validation**: Ensures compliance with each normal form before advancing to the next.

## Project Structure

```plaintext
.
├── Dependency.py        # Manages functional and multivalued dependencies
├── Input.py             # Handles input data from Excel files
├── Main.py              # Main script that initiates the normalization process
├── Normalization.py     # Core normalization logic for each normal form
├── Relation.py          # Defines the Relation class and related methods
├── relation.xlsx        # Example input file with initial schema data
├── relationinput.xlsx   # Additional input file example
├── relationinput2.xlsx  # Another example input file
├── FD.txt               # Lists functional dependencies
├── FD2.txt              # Lists functional dependencies for other tables
└── requirements.txt     # Lists required Python packages

