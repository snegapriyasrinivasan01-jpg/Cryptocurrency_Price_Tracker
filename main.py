import os
from scraper import scrape_crypto_data

def save_to_csv(df, filepath="crypto_prices.csv"):
    file_exists = os.path.isfile(filepath)
    df.to_csv(filepath, mode="a", index=False, header=not file_exists)
    print(f"\n[✓] Data successfully saved to {filepath}")

def main():
    print("=" * 60)
    print("        CRYPTOCURRENCY PRICE TRACKER")
    print("=" * 60)
    print("\nFetching cryptocurrency data...")

    crypto_df = scrape_crypto_data(headless=True, top_n=10)

    if not crypto_df.empty:
        print("\n--- Live Market Data ---")
        print(crypto_df.to_string(index=False))
        save_to_csv(crypto_df)
    else:
        print("\n[X] Unable to retrieve data. Check network settings.")

if __name__ == "__main__":
    main()