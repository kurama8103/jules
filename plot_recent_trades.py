import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def fetch_recent_trades(product_code="BTC_JPY", count=500):
    """
    Fetches the most recent trades from the bitflyer API.
    """
    url = f"https://api.bitflyer.com/v1/getexecutions"
    params = {
        "product_code": product_code,
        "count": count
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trades for {product_code}: {e}")
        return None

def fetch_funding_rate(product_code="FX_BTC_JPY"):
    """
    Gets the funding rate for a given product code from bitflyer.
    """
    url = f"https://api.bitflyer.com/v1/getfundingrate?product_code={product_code}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching funding rate for {product_code}: {e}")
        return None

def plot_trades(spot_df=None, futures_df=None, funding_rate=None, output_filename="recent_trades.png"):
    """
    Plots the trade data for spot and futures and saves it to a file.
    Displays the funding rate in the title.
    """
    if (spot_df is None or spot_df.empty) and (futures_df is None or futures_df.empty):
        print("All trade data is empty, skipping plot.")
        return

    print(f"Generating plot and saving to {output_filename}...")
    fig, ax = plt.subplots(figsize=(15, 7))

    # Plotting
    if spot_df is not None and not spot_df.empty:
        ax.plot(spot_df['exec_date'], spot_df['price'], marker='.', linestyle='-', markersize=4, label='Spot (BTC/JPY)')
    if futures_df is not None and not futures_df.empty:
        ax.plot(futures_df['exec_date'], futures_df['price'], marker='.', linestyle='-', markersize=4, label='Futures (FX_BTC_JPY)')

    # Formatting the plot
    title = 'Recent Trades on bitflyer'
    if funding_rate is not None:
        title += f' | Current Funding Rate: {funding_rate:.8f}'
    ax.set_title(title)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price (JPY)')
    ax.grid(True)
    ax.legend()

    # Improve date formatting on x-axis
    fig.autofmt_xdate()
    formatter = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(formatter)

    try:
        plt.savefig(output_filename)
        print(f"Successfully saved plot to {output_filename}")
    except Exception as e:
        print(f"Error saving plot: {e}")


def main():
    """
    Main function to fetch and plot recent trades.
    """
    print("Fetching data from bitflyer API...")
    spot_trades = fetch_recent_trades(product_code="BTC_JPY")
    futures_trades = fetch_recent_trades(product_code="FX_BTC_JPY")
    funding_rate_data = fetch_funding_rate()

    # --- Process Data ---
    def process_trades(trades, name):
        if not trades:
            print(f"Could not fetch {name} trades.")
            return None
        df = pd.DataFrame(trades)
        df['exec_date'] = pd.to_datetime(df['exec_date'], format='ISO8601')
        df = df.sort_values(by='exec_date')
        print(f"Successfully processed {len(df)} {name} trades.")
        return df

    spot_df = process_trades(spot_trades, "Spot (BTC_JPY)")
    futures_df = process_trades(futures_trades, "Futures (FX_BTC_JPY)")

    funding_rate = None
    if funding_rate_data and 'current_funding_rate' in funding_rate_data:
        funding_rate = funding_rate_data['current_funding_rate']
        print(f"Current funding rate: {funding_rate}")
    else:
        print("Could not fetch funding rate.")

    # --- Plot Data ---
    if spot_df is not None or futures_df is not None:
        # Pass the DataFrames to the plotting function
        plot_trades(spot_df, futures_df, funding_rate)
    else:
        print("No trade data available to plot. Exiting.")

    print("Script finished.")

if __name__ == "__main__":
    main()
