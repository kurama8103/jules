import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import database # New import

# --- Configuration ---
SPOT_PRODUCT_CODE = "BTC_JPY"
FUTURES_PRODUCT_CODE = "FX_BTC_JPY"

# --- API Fetching ---

def fetch_new_trades(product_code: str, after_id: int | None = None):
    """
    Fetches trades from the bitflyer API that occurred after a given trade ID.
    If after_id is None, it fetches the most recent trades.
    """
    url = f"https://api.bitflyer.com/v1/getexecutions"
    params = {
        "product_code": product_code,
        "count": 500 # Always fetch the max count
    }
    if after_id:
        params['after'] = after_id

    print(f"Fetching trades for {product_code} after ID: {after_id or 'None'}...")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        trades = response.json()
        # API returns in ascending order of ID, which is what we want.
        return trades
    except requests.exceptions.RequestException as e:
        print(f"Error fetching new trades for {product_code}: {e}")
        return None

def fetch_funding_rate(product_code="FX_BTC_JPY"):
    """
    Gets the current funding rate from bitflyer.
    """
    url = f"https://api.bitflyer.com/v1/getfundingrate?product_code={product_code}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching funding rate for {product_code}: {e}")
        return None


# --- Data Processing ---

def calculate_spread(spot_df: pd.DataFrame, futures_df: pd.DataFrame, interval='1s') -> pd.DataFrame:
    """
    Resamples spot and futures data to a common time interval and calculates the spread.
    """
    if spot_df.empty or futures_df.empty:
        return pd.DataFrame()

    # Convert UTC index to Tokyo time
    spot_df.index = spot_df.index.tz_convert('Asia/Tokyo')
    futures_df.index = futures_df.index.tz_convert('Asia/Tokyo')

    # Resample to the given interval, taking the last price and forward-filling
    spot_resampled = spot_df['price'].resample(interval).last().ffill()
    futures_resampled = futures_df['price'].resample(interval).last().ffill()

    # Combine into a single DataFrame
    combined_df = pd.concat([spot_resampled, futures_resampled], axis=1, keys=['spot_price', 'futures_price'])

    # Drop rows where we don't have both prices
    combined_df.dropna(inplace=True)

    # Calculate spread percentage
    combined_df['spread_pct'] = ((combined_df['futures_price'] - combined_df['spot_price']) / combined_df['spot_price']) * 100

    print(f"Calculated spread for {len(combined_df)} time intervals.")
    return combined_df


# --- Plotting ---

def plot_trades(processed_df: pd.DataFrame, funding_rate: float | None = None, output_filename="trade_analyzer.png"):
    """
    Plots prices and spread in two vertically stacked subplots.
    """
    if processed_df.empty:
        print("Processed data is empty, skipping plot.")
        return

    print(f"Generating stacked plot and saving to {output_filename}...")
    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        sharex=True,
        figsize=(18, 10),
        gridspec_kw={'height_ratios': [3, 1]}
    )

    # --- Top Plot (Prices) ---
    ax1.plot(processed_df.index, processed_df['spot_price'], color='tab:blue', label='Spot Price')
    ax1.plot(processed_df.index, processed_df['futures_price'], color='tab:cyan', linestyle='--', label='Futures Price')
    ax1.set_ylabel('Price (JPY)')
    ax1.legend()
    ax1.grid(True)

    # --- Bottom Plot (Spread) ---
    ax2.plot(processed_df.index, processed_df['spread_pct'], color='tab:red', label='Spread %')
    ax2.axhline(0, color='tab:red', linestyle='--', linewidth=0.8)
    ax2.set_ylabel('Spread (%)')
    ax2.set_xlabel('Time (JST)')
    ax2.grid(True)

    # --- Figure-level Formatting ---
    title = 'bitflyer Spot vs. Futures Analysis'
    if funding_rate is not None:
        title += f'\nCurrent Funding Rate: {funding_rate:.8f}'
    fig.suptitle(title, fontsize=16)

    fig.tight_layout(rect=[0, 0.03, 1, 0.97]) # Adjust layout to make room for suptitle

    # Date formatting for the shared x-axis
    formatter = mdates.DateFormatter('%H:%M:%S', tz='Asia/Tokyo')
    ax2.xaxis.set_major_formatter(formatter)

    try:
        plt.savefig(output_filename)
        print(f"Successfully saved plot to {output_filename}")
    except Exception as e:
        print(f"Error saving plot: {e}")


# --- Main Execution Logic ---

def main():
    """
    Main function to fetch, store, and analyze trade data.
    """
    # 1. Initialize Database
    database.initialize_database()

    products_to_sync = [SPOT_PRODUCT_CODE, FUTURES_PRODUCT_CODE]

    # 2. Sync data for each product
    for product in products_to_sync:
        print(f"\n--- Syncing for {product} ---")
        latest_id = database.get_latest_trade_id(product)
        new_trades = fetch_new_trades(product, after_id=latest_id)
        if new_trades:
            database.save_trades(new_trades, product)
        else:
            print(f"No new trades found for {product}.")

    # 3. Load all data from DB for analysis
    print("\n--- Loading all data from database for analysis ---")
    spot_df = database.load_all_trades_as_df(SPOT_PRODUCT_CODE)
    futures_df = database.load_all_trades_as_df(FUTURES_PRODUCT_CODE)

    # 4. Process data and calculate spread
    processed_df = calculate_spread(spot_df, futures_df)

    # 5. Fetch current funding rate
    funding_rate_data = fetch_funding_rate()
    funding_rate = funding_rate_data.get('current_funding_rate') if funding_rate_data else None

    # 6. Call plotting function
    if not processed_df.empty:
        plot_trades(processed_df, funding_rate)

    print("\nScript finished.")


if __name__ == "__main__":
    main()
