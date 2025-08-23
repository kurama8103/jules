import requests
import json

def get_ticker(product_code):
    """
    Gets the ticker for a given product code from bitflyer.
    """
    url = f"https://api.bitflyer.com/v1/getticker?product_code={product_code}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ticker for {product_code}: {e}")
        return None

def get_funding_rate(product_code):
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

def main():
    """
    Main function to calculate and display arbitrage information.
    """
    # Get Spot Price (BTC/JPY)
    spot_ticker = get_ticker("BTC_JPY")
    if not spot_ticker:
        return
    spot_price = spot_ticker.get('ltp')

    # Get Futures Price (FX_BTC_JPY)
    futures_ticker = get_ticker("FX_BTC_JPY")
    if not futures_ticker:
        return
    futures_price = futures_ticker.get('ltp')

    # Get Funding Rate
    funding_rate_data = get_funding_rate("FX_BTC_JPY")
    if not funding_rate_data:
        return
    funding_rate = funding_rate_data.get('current_funding_rate')

    if spot_price is None or futures_price is None or funding_rate is None:
        print("Could not retrieve all necessary data. Exiting.")
        return

    # Calculate spread
    spread = futures_price - spot_price
    spread_percentage = (spread / spot_price) * 100 if spot_price != 0 else 0

    # Display information
    print("--- bitflyer Arbitrage Calculator ---")
    print(f"Spot Price (BTC/JPY):      {spot_price:,.2f} JPY")
    print(f"Futures Price (FX_BTC_JPY): {futures_price:,.2f} JPY")
    print(f"Spread:                    {spread:,.2f} JPY ({spread_percentage:.4f}%)")
    print(f"Funding Rate:              {funding_rate:.8f}")
    print("-------------------------------------")

    # Simple arbitrage logic
    # This is a very simplified logic and does not account for fees,
    # slippage, or the timing of funding payments.
    # A positive funding rate means longs pay shorts.
    # A negative funding rate means shorts pay longs.
    # The SFD (Swap For Difference) is applied when the spread is >= 5%.
    # For this simplified example, we'll just look at the spread.

    if spread_percentage > 0.1: # Threshold for potential profit, considering fees.
        print("\nRecommendation: Potential arbitrage opportunity.")
        print("Strategy: Sell Futures (Short) and Buy Spot (Long).")
        print("You would potentially profit from the price difference and/or receive funding payments if the funding rate is positive for shorts.")
    elif spread_percentage < -0.1:
        print("\nRecommendation: Potential arbitrage opportunity.")
        print("Strategy: Buy Futures (Long) and Sell Spot (Short).")
        print("You would potentially profit from the price difference and/or receive funding payments if the funding rate is positive for longs.")
    else:
        print("\nNo significant arbitrage opportunity detected at the moment.")

if __name__ == "__main__":
    main()
