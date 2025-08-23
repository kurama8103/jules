import ccxt
import requests
import time
import datetime

# --- Configuration ---
# The symbol to watch for arbitrage opportunities.
# Note: GMO Coin uses 'BTC_JPY', while ccxt uses 'BTC/JPY'. The code handles this.
SYMBOL_CCXT = 'BTC/JPY'
SYMBOL_GMO = 'BTC_JPY'

# The profit threshold in JPY to trigger an alert.
# This is the difference between the selling price and the buying price.
PROFIT_THRESHOLD = 5000  # 5000 JPY

# The interval in seconds to wait between checking prices.
REFRESH_INTERVAL_SECONDS = 10

# --- Exchange API Functions ---

def get_bitflyer_price(symbol):
    """Fetches the latest ticker price from bitFlyer."""
    try:
        bitflyer = ccxt.bitflyer()
        ticker = bitflyer.fetch_ticker(symbol)
        return {'exchange': 'bitFlyer', 'bid': ticker['bid'], 'ask': ticker['ask']}
    except Exception as e:
        print(f"Error fetching from bitFlyer: {e}")
        return None

def get_bitbank_price(symbol):
    """Fetches the latest ticker price from bitbank."""
    try:
        bitbank = ccxt.bitbank()
        ticker = bitbank.fetch_ticker(symbol)
        return {'exchange': 'bitbank', 'bid': ticker['bid'], 'ask': ticker['ask']}
    except Exception as e:
        print(f"Error fetching from bitbank: {e}")
        return None

def get_gmocoin_price(symbol):
    """Fetches the latest ticker price from GMO Coin."""
    url = f"https://api.coin.z.com/public/v1/ticker?symbol={symbol}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 0 and data['data']:
            ticker = data['data'][0]
            return {'exchange': 'GMO Coin', 'bid': float(ticker['bid']), 'ask': float(ticker['ask'])}
        else:
            print(f"Error in GMO Coin API response: {data.get('messages')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from GMO Coin: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred with GMO Coin: {e}")
        return None

# --- Core Arbitrage Logic ---

def find_arbitrage_opportunity(prices):
    """
    Finds an arbitrage opportunity from a list of prices.
    An opportunity exists if the highest bid is greater than the lowest ask.
    """
    if len(prices) < 2:
        return None, None

    # Find the best price to buy at (lowest ask) and sell at (highest bid)
    lowest_ask_exchange = min(prices, key=lambda x: x['ask'])
    highest_bid_exchange = max(prices, key=lambda x: x['bid'])

    lowest_ask_price = lowest_ask_exchange['ask']
    highest_bid_price = highest_bid_exchange['bid']

    # Check if we can buy low and sell high for a profit
    if highest_bid_price > lowest_ask_price:
        profit = highest_bid_price - lowest_ask_price
        return {
            'buy_at': lowest_ask_exchange['exchange'],
            'buy_price': lowest_ask_price,
            'sell_at': highest_bid_exchange['exchange'],
            'sell_price': highest_bid_price,
            'profit': profit
        }, prices

    return None, prices

def print_prices(prices):
    """Prints a formatted table of current prices."""
    print(f"\n--- Prices at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    if not prices:
        print("No price data available.")
        return

    print(f"{'Exchange':<12} | {'Bid (JPY)':<15} | {'Ask (JPY)':<15}")
    print("-" * 47)
    for price in prices:
        print(f"{price['exchange']:<12} | {price['bid']:<15,.0f} | {price['ask']:<15,.0f}")
    print("-" * 47)


if __name__ == "__main__":
    print("Starting arbitrage bot...")
    print(f"Watching symbol: {SYMBOL_CCXT}")
    print(f"Profit threshold: {PROFIT_THRESHOLD:,.0f} JPY")
    print(f"Refresh interval: {REFRESH_INTERVAL_SECONDS} seconds")

    while True:
        try:
            # Fetch prices from all exchanges
            price_data = [
                get_bitflyer_price(SYMBOL_CCXT),
                get_bitbank_price(SYMBOL_CCXT),
                get_gmocoin_price(SYMBOL_GMO)
            ]

            # Filter out any failed requests
            valid_prices = [p for p in price_data if p is not None]

            print_prices(valid_prices)

            # Find and report arbitrage opportunities
            opportunity, _ = find_arbitrage_opportunity(valid_prices)

            if opportunity:
                if opportunity['profit'] >= PROFIT_THRESHOLD:
                    print("\n" + "!"*60)
                    print(f"  !!! ARBITRAGE OPPORTUNITY DETECTED !!!")
                    print(f"  Buy at:    {opportunity['buy_at']} for {opportunity['buy_price']:,.0f} JPY")
                    print(f"  Sell at:   {opportunity['sell_at']} for {opportunity['sell_price']:,.0f} JPY")
                    print(f"  Potential Profit: {opportunity['profit']:,.2f} JPY")
                    print("!"*60 + "\n")
                else:
                    # Optional: Print smaller, non-alert-worthy opportunities
                    print(f"Minor opportunity found: Profit of {opportunity['profit']:,.2f} JPY (below threshold).")

            else:
                print("No arbitrage opportunity found.")

            # Wait for the next refresh cycle
            time.sleep(REFRESH_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\nStopping arbitrage bot.")
            break
        except Exception as e:
            print(f"An unexpected error occurred in the main loop: {e}")
            time.sleep(REFRESH_INTERVAL_SECONDS)
