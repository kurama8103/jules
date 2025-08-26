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

def plot_trades(trades_df, output_filename="recent_trades.png"):
    """
    Plots the trade data and saves it to a file.
    """
    if trades_df.empty:
        print("Trade data is empty, skipping plot.")
        return

    print(f"Generating plot and saving to {output_filename}...")
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(trades_df['exec_date'], trades_df['price'], marker='.', linestyle='-', markersize=4)

    # Formatting the plot
    ax.set_title('Recent BTC/JPY Trades on bitflyer')
    ax.set_xlabel('Time')
    ax.set_ylabel('Price (JPY)')
    ax.grid(True)

    # Improve date formatting on x-axis
    fig.autofmt_xdate() # Auto-rotates dates to fit
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
    print("Fetching recent trades for BTC_JPY...")
    trades = fetch_recent_trades()

    if trades:
        # Create a pandas DataFrame
        df = pd.DataFrame(trades)

        # Convert exec_date to datetime objects
        # Using format='ISO8601' handles timestamps with and without fractional seconds.
        df['exec_date'] = pd.to_datetime(df['exec_date'], format='ISO8601')

        # Sort by date just in case the API doesn't guarantee order
        df = df.sort_values(by='exec_date')

        print(f"Successfully fetched and processed {len(df)} trades.")

        # Pass the DataFrame to the plotting function
        plot_trades(df)

    else:
        print("Could not fetch trades. Exiting.")

    print("Script finished.")

if __name__ == "__main__":
    main()
