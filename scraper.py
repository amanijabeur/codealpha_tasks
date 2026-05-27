"""
========================================================================
TASK 1: Yahoo Finance 100 Most Active Stocks Scraper (HTML Table Engine)
========================================================================
Fulfills task requirements by targeting strict HTML table structures.
Parses combined text nodes directly into clean, native Excel columns.
========================================================================
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import re

# ── LOGGING SETUP ─────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

TARGET_URL = "https://finance.yahoo.com/markets/stocks/most-active/?count=100"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

def main():
    print("=" * 60)
    print("   Yahoo Finance 100 Most Active Stocks (Pure HTML Engine)")
    print("=" * 60)

    logger.info("Connecting to Yahoo Finance web view...")
    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Network connection failed: {e}")
        return

    # 1. HTML TARGETING - Mandated by assignment constraints
    soup = BeautifulSoup(response.text, "html.parser")
    
    logger.info("Scanning for core <table> layout arrays...")
    table = soup.find("table")
    
    if not table:
        logger.error("Could not find any <table> element on the webpage.")
        return

    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")
    
    logger.info(f"BeautifulSoup located {len(rows)} data rows inside the DOM matrix.")

    parsed_stocks = []

    for row in rows:
        cols = row.find_all("td")
        # Ensure we skip header rows or broken layout elements
        if len(cols) < 3:
            continue

        try:
            # Column 0: Symbol Ticker
            symbol = cols[0].get_text(strip=True)
            
            # Column 1: Company Name / Long Name
            name = cols[1].get_text(strip=True).replace(",", "")
            
            # --- THE CLEANUP ENGINE ---
            # Instead of trusting a specific index position, we grab all text 
            # within the remaining cells to handle dynamic layout shifts.
            full_row_text = " ".join([c.get_text(" ", strip=True) for c in cols[2:]])
            
            # Use a robust regular expression to pull out the numeric details:
            # - Price: The first decimal number it encounters
            # - Change: The second decimal number (which can be positive or negative)
            # - % Change: The percentage value wrapped inside parentheses
            numbers = re.findall(r'[-+]?\d?[\d,]*\.\d+', full_row_text)
            pct_match = re.search(r'\(([-+]?[\d,]*\.\d+)%\)', full_row_text)

            if len(numbers) >= 2:
                price = numbers[0]
                change = numbers[1]
            else:
                # Basic backup indexing if the regex doesn't find a match
                price = cols[2].get_text(strip=True)
                change = cols[3].get_text(strip=True) if len(cols) > 3 else "0"

            pct_change = pct_match.group(1) if pct_match else (cols[4].get_text(strip=True) if len(cols) > 4 else "0")

            # Clean out lingering layout characters
            pct_change = pct_change.replace("%", "").replace("(", "").replace(")", "").strip()

            if symbol and symbol.lower() != "symbol":
                parsed_stocks.append({
                    "Symbol": symbol,
                    "Company Name": name,
                    "Price": price,
                    "Change": change,
                    "% Change": pct_change
                })
        except Exception as e:
            continue

    # 2. DATA PROCESSING FRAMEWORK
    final_df = pd.DataFrame(parsed_stocks)

    if final_df.empty:
        logger.error("Failed to parse the data points into the structured grid.")
        return

    # Convert columns to numeric types so they format properly in Excel
    final_df["Price"] = pd.to_numeric(final_df["Price"].astype(str).str.replace(",", "", regex=False), errors="coerce")
    final_df["Change"] = pd.to_numeric(final_df["Change"], errors="coerce")
    final_df["% Change"] = pd.to_numeric(final_df["% Change"], errors="coerce")

    # Generate the final native Excel file
    output_path = "most_active_stocks_dataset.xlsx"
    final_df.to_excel(output_path, index=False, engine="openpyxl")
    
    print("\n" + "=" * 60)
    print(" PROCESS MATRIX COMPLETE")
    print("=" * 60)
    print(f"Workbook successfully saved → {output_path}")
    print(f"Total Rows Saved: {len(final_df)}")
    print("\nClean Grid Preview Layout:")
    print(final_df.head(5).to_string())

if __name__ == "__main__":
    main()