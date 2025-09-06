import requests

def get_ticker(product_code):
    """Gets the ticker for a given product code from bitflyer."""
    url = f"https://api.bitflyer.com/v1/getticker?product_code={product_code}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # In a real app, you might want to log this instead of printing
        # For this tool, printing is fine.
        return {'error': str(e)}

def get_funding_rate(product_code):
    """Gets the funding rate for a given product code from bitflyer."""
    url = f"https://api.bitflyer.com/v1/getfundingrate?product_code={product_code}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def get_arbitrage_analysis() -> str:
    """
    Fetches data, performs arbitrage calculation, and returns the result as a formatted string.
    """
    spot_ticker = get_ticker("BTC_JPY")
    futures_ticker = get_ticker("FX_BTC_JPY")
    funding_rate_data = get_funding_rate("FX_BTC_JPY")

    if 'error' in spot_ticker or 'error' in futures_ticker or 'error' in funding_rate_data:
        return "Error fetching data from bitflyer API."

    spot_price = spot_ticker.get('ltp')
    futures_price = futures_ticker.get('ltp')
    funding_rate = funding_rate_data.get('current_funding_rate')

    if spot_price is None or futures_price is None or funding_rate is None:
        return "Could not retrieve all necessary data points."

    spread = futures_price - spot_price
    spread_percentage = (spread / spot_price) * 100 if spot_price != 0 else 0

    # Build the result string
    output = []
    output.append("--- bitflyer Arbitrage Analysis ---")
    output.append(f"Spot Price (BTC/JPY):      {spot_price:,.2f} JPY")
    output.append(f"Futures Price (FX_BTC_JPY): {futures_price:,.2f} JPY")
    output.append(f"Spread:                    {spread:,.2f} JPY ({spread_percentage:.4f}%)")
    output.append(f"Funding Rate:              {funding_rate:.8f}")
    output.append("-------------------------------------")

    if spread_percentage > 0.1:
        output.append("\nRecommendation: Potential arbitrage opportunity.")
        output.append("Strategy: Sell Futures (Short) and Buy Spot (Long).")
    elif spread_percentage < -0.1:
        output.append("\nRecommendation: Potential arbitrage opportunity.")
        output.append("Strategy: Buy Futures (Long) and Sell Spot (Short).")
    else:
        output.append("\nNo significant arbitrage opportunity detected at the moment.")

    return "\n".join(output)

def main():
    """
    For direct command-line execution.
    Fetches, calculates, and prints the arbitrage analysis.
    """
    analysis_result = get_arbitrage_analysis()
    print(analysis_result)

if __name__ == "__main__":
    main()
