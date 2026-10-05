# Restaurant Sales Data Cleaning

A small Python and pandas project for cleaning the `restaurant_sales_data.csv` dataset. This project is designed to be used in VS Code.

## Overview

This project reads the raw restaurant sales CSV, cleans missing and inconsistent values, validates totals, and writes a cleaned CSV file.

- **Input:** `restaurant_sales_data.csv`
- **Output:** `restaurant_sales_data_cleaned.csv`
- **Main script:** `clean_data.py`

## Requirements

- Python 3.9 or newer
- pandas
- numpy
- VS Code (recommended)
- VS Code Python extension
- VS Code Jupyter extension (optional, for notebooks)

## Setup

Open the project folder in VS Code, then open a terminal.

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install pandas numpy
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy
```

## Usage

1. Place `restaurant_sales_data.csv` in the project root.
2. Make sure `clean_data.py` is in the same folder.
3. Run:

```bash
python clean_data.py
```

4. The cleaned file will be created as:

```text
restaurant_sales_data_cleaned.csv
```

## What the Script Does

The cleaning script:

1. Reads all columns as strings first so IDs and dates are not auto-corrupted.
2. Trims whitespace from text columns.
3. Converts blank-like values such as `""`, `"nan"`, `"NULL"`, and `"None"` to proper missing values.
4. Converts `Price`, `Quantity`, and `Order Total` to numeric values.
5. Converts `Order Date` to a real datetime value.
6. Removes rows with missing `Order ID` or invalid `Order Date`.
7. Removes exact duplicate rows.
8. Fills missing `Price`, `Quantity`, or `Order Total` using arithmetic when possible:
   - `Price = Order Total / Quantity`
   - `Quantity = Order Total / Price`
   - `Order Total = Price * Quantity`
9. Infers missing `Category` from `Item` using known item-to-category mappings.
10. Fills remaining missing text values with clear labels:
    - `Unknown Item`
    - `Unknown Category`
    - `Unknown`
11. Standardizes text formatting for `Category`, `Item`, and `Payment Method`.
12. Adds two validation columns:
    - `Expected Total`
    - `Total Mismatch`
13. Saves the cleaned data to a new CSV file.

## Output Columns

The cleaned CSV contains these columns:

| Column | Description |
|---|---|
| `Order ID` | Unique order identifier |
| `Customer ID` | Customer identifier |
| `Category` | Menu category, such as Main Dishes or Drinks |
| `Item` | Menu item name |
| `Price` | Item price |
| `Quantity` | Quantity ordered |
| `Order Total` | Total amount for the order line |
| `Order Date` | Date of the order |
| `Payment Method` | Payment method used |
| `Expected Total` | Calculated as `Price * Quantity` |
| `Total Mismatch` | `True` if `Order Total` does not match `Expected Total` |

## Notes

- The original input file is never modified.
- If you want to drop rows that have no usable sales numbers at all, open `clean_data.py` and uncomment this line:

```python
# df = df.dropna(subset=["Price", "Quantity", "Order Total"], how="all")
```

- A `Total Mismatch` value of `True` means the recorded `Order Total` does not equal `Price * Quantity`.

## Project Structure

```text
.
├── restaurant_sales_data.csv
├── clean_data.py
├── restaurant_sales_data_cleaned.csv
└── README.md
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'pandas'`

Make sure your virtual environment is activated, then install dependencies:

```bash
pip install pandas numpy
```

### The script cannot find the CSV file

Make sure `restaurant_sales_data.csv` is in the same folder as `clean_data.py`.

### Dates are not parsed correctly

Check that the `Order Date` column uses a recognizable format such as:

```text
2023-12-21
```

If your dates use a different format, update this line in `clean_data.py`:

```python
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
```

For example:

```python
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce", dayfirst=True)
```

## License

This project is provided for personal and educational use.