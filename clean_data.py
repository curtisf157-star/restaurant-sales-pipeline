import pandas as pd

# --- 1. Load the file ---
df = pd.read_csv("restaurant_sales_data.csv")
rows_before = len(df)

# --- 2. Look at what's wrong ---
print("=== BEFORE CLEANING ===")
print("Rows:", rows_before)
print("\nMissing values per column:")
print(df.isnull().sum())

# --- 3. Clean it up ---

# Strip spaces from column names
df.columns = df.columns.str.strip()

# Remove exact duplicate rows
df = df.drop_duplicates()

# Strip extra spaces from text columns
for col in ["Category", "Item", "Payment Method"]:
    df[col] = df[col].astype("string").str.strip()

# Fill blank text with "Unknown"
df["Category"] = df["Category"].fillna("Unknown")
df["Item"] = df["Item"].fillna("Unknown")
df["Payment Method"] = df["Payment Method"].fillna("Unknown")

# Convert Order Date from text to a real date
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

# Drop rows where Price, Quantity AND Order Total are ALL missing
df = df.dropna(subset=["Price", "Quantity", "Order Total"], how="all")

# Quantity and Order Total are whole numbers -> make them integers
df["Quantity"] = df["Quantity"].astype("Int64")
# Price has decimals (2.5, 12.5) -> keep as float, round to 2 dp
df["Price"] = df["Price"].round(2)
# --- 3b. Back-calculate missing Prices ---
# Order Total = Price × Quantity, so Price = Order Total ÷ Quantity
mask = df["Price"].isnull() & df["Quantity"].notnull() & df["Order Total"].notnull()
df.loc[mask, "Price"] = (df.loc[mask, "Order Total"] / df.loc[mask, "Quantity"]).round(2)

# Flag any rows still missing a Price
df["Price_Missing"] = df["Price"].isnull()
# --- 4. Save the cleaned file ---
df.to_csv("restaurant_sales_data_clean.csv", index=False)

# --- 5. Show the result ---
print("\n=== AFTER CLEANING ===")
print("Rows:", len(df))
print("\nMissing values per column:")
print(df.isnull().sum())
print("\nSaved to: restaurant_sales_data_clean.csv")
print("\nFirst 5 rows of cleaned data:")
print(df.head())