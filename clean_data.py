"""
Clean the raw South African used-vehicle listings and write the file Power BI loads.

Usage (from the repository root):
    python clean_data.py

Input : data/raw/SA_Used_Vehicle_Market_RAW.csv
Output: data/clean/SA_Used_Vehicle_Market_CLEAN.xlsx  (sheets: Fact_Vehicles, Cleaning_Log)

Numbers are written as real numbers and dates as real dates, so Power BI does not
have to parse text (this avoids decimal-separator errors on South African locales).
"""
from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path("data/raw/SA_Used_Vehicle_Market_RAW.csv")
OUT = Path("data/clean/SA_Used_Vehicle_Market_CLEAN.xlsx")

# Validation rules
YEAR_MIN, YEAR_MAX = 2014, 2026          # 1900/2035/2050 are impossible; one 2010 car was an outlier
PRICE_MIN, PRICE_MAX = 30_000, 2_000_000  # R5k/R25k and R4.5M/R9.99M are placeholders or typos
MILEAGE_MAX = 500_000                     # km; <= 0 or above this is set to blank
PLACEHOLDER_KM, PLACEHOLDER_PRICE = 2_500, 59_900
PREMIUM_BRANDS = {"BMW", "Mercedes-Benz", "Audi", "Volvo", "Land Rover"}  # used in Power BI (Dim_Brand)


def fix_brand(name: str) -> str:
    return name.upper() if name.upper() in {"BMW", "BYD", "GWM"} else name.title()


def main() -> None:
    raw = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    log = [("Raw rows", len(raw))]
    df = raw.copy()

    # 1. Trim whitespace everywhere
    for col in df.columns:
        df[col] = df[col].str.strip()

    # 2. Standardise text
    df["Brand"] = df["Brand"].map(fix_brand)
    df["Fuel_Type"] = df["Fuel_Type"].str.title()
    df["Transmission"] = df["Transmission"].str.title()
    df["Province"] = df["Province"].str.title().replace({"Kwazulu-Natal": "KwaZulu-Natal"})

    # 3. Data types
    for col in ["Year", "Price_ZAR", "Mileage_KM", "Previous_Owners", "Engine_Size_L"]:
        df[col] = pd.to_numeric(df[col].replace("", np.nan))
    df["Listing_Date"] = pd.to_datetime(df["Listing_Date"])

    # 4. Remove duplicates and impossible rows
    n = len(df)
    df = df.drop_duplicates("Vehicle_ID")
    log.append(("Duplicate rows removed", n - len(df)))

    n = len(df)
    df = df[df["Year"].between(YEAR_MIN, YEAR_MAX)]
    log.append((f"Removed: impossible or outlier year (outside {YEAR_MIN}-{YEAR_MAX})", n - len(df)))

    n = len(df)
    df = df[df["Price_ZAR"].between(PRICE_MIN, PRICE_MAX)]
    log.append((f"Removed: impossible price (outside R{PRICE_MIN:,}-R{PRICE_MAX:,})", n - len(df)))

    # 5. Blank out bad values instead of dropping the whole row
    bad_km = (df["Mileage_KM"] <= 0) | (df["Mileage_KM"] > MILEAGE_MAX)
    df.loc[bad_km, "Mileage_KM"] = np.nan
    log.append((f"Mileage set to blank (<= 0 or > {MILEAGE_MAX:,} km)", int(bad_km.sum())))

    ev_zero = df["Engine_Size_L"] == 0
    df.loc[ev_zero, "Engine_Size_L"] = np.nan
    log.append(("Engine size 0.0 set to blank (electric vehicles)", int(ev_zero.sum())))

    # 6. Fill blank text fields
    for col in ["City", "Colour", "Service_History"]:
        blanks = int((df[col] == "").sum())
        df[col] = df[col].replace("", "Unknown")
        log.append((f"{col} blank -> 'Unknown'", blanks))

    # 7. Derived columns
    df["Vehicle_Age"] = df["Listing_Date"].dt.year - df["Year"]
    df["Age_Band"] = pd.cut(df["Vehicle_Age"], [-1, 2, 5, 8, 99],
                            labels=["0-2 yrs", "3-5 yrs", "6-8 yrs", "9+ yrs"]).astype(str)
    mileage_band = pd.cut(df["Mileage_KM"], [-1, 19_999.99, 49_999.99, 99_999.99, 149_999.99, 1e9],
                          labels=["1. Under 20k", "2. 20-50k", "3. 50-100k", "4. 100-150k", "5. 150k+"]).astype(object)
    df["Mileage_Band"] = mileage_band.where(df["Mileage_KM"].notna(), "Unknown")
    df["Price_Band"] = pd.cut(df["Price_ZAR"], [0, 149_999.99, 299_999.99, 499_999.99, 1e9],
                              labels=["1. Under R150k", "2. R150k-300k", "3. R300k-500k", "4. R500k+"]).astype(str)
    df["Make_Model"] = df["Brand"] + " " + df["Model"]
    df["Placeholder_Flag"] = np.where(
        (df["Mileage_KM"] == PLACEHOLDER_KM) | (df["Price_ZAR"] == PLACEHOLDER_PRICE), "Yes", "No")

    for col in ["Year", "Price_ZAR", "Mileage_KM", "Previous_Owners", "Vehicle_Age"]:
        df[col] = df[col].astype("Int64")
    df = df.reset_index(drop=True)

    log.append(("Clean rows", len(df)))
    log.append(("Rows flagged Placeholder_Flag = Yes (kept)", int((df["Placeholder_Flag"] == "Yes").sum())))

    # 8. Write the output
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(OUT, engine="openpyxl", datetime_format="yyyy-mm-dd",
                        date_format="yyyy-mm-dd") as writer:
        df.to_excel(writer, sheet_name="Fact_Vehicles", index=False)
        pd.DataFrame(log, columns=["Step", "Rows"]).to_excel(writer, sheet_name="Cleaning_Log", index=False)

    print(pd.DataFrame(log, columns=["Step", "Rows"]).to_string(index=False))
    print(f"\nSaved {OUT}")


if __name__ == "__main__":
    main()
