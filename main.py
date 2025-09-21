import time
import sys
from src.gmo_coin import api_client as gmo_client
from src.bitbank import api_client as bitbank_client
from src.arbitrage import calculator
from src.data_logger import logger

try:
    import config
except ImportError:
    print("ERROR: config.py not found.")
    print("Please copy config.py.example to config.py and fill in your settings.")
    sys.exit(1)

def main():
    print("Starting arbitrage bot...")

    while True:
        for symbol in config.TARGET_SYMBOLS:
            bitbank_symbol = symbol.lower()
            gmo_symbol = symbol

            print(f"--- Fetching data for {gmo_symbol} at {time.ctime()} ---")

            gmo_ticker = gmo_client.get_ticker(gmo_symbol)
            bitbank_ticker = bitbank_client.get_ticker(bitbank_symbol)

            if gmo_ticker and bitbank_ticker:
                logger.log_ticker_data(gmo_symbol, gmo_ticker, bitbank_ticker)

                opportunities = calculator.calculate_arbitrage(gmo_ticker, bitbank_ticker)

                if opportunities:
                    print(f"Arbitrage opportunities found for {gmo_symbol}!")
                    for opp in opportunities:
                        # ログに記録
                        logger.log_opportunity(gmo_symbol, opp)
                        # コンソールに表示
                        print(f"  Buy at {opp['buy_exchange']} for {opp['buy_price']:.2f}")
                        print(f"  Sell at {opp['sell_exchange']} for {opp['sell_price']:.2f}")
                        print(f"  Gross Profit (Spread): {opp['gross_profit']:.2f} JPY")
                        print(f"  Total Cost (Fees): {opp['total_cost']:.2f} JPY")
                        print(f"  Net Profit: {opp['net_profit']:.2f} JPY")
                        print(f"  Net Profit Rate: {opp['profit_rate']:.4%}")
                else:
                    print(f"No arbitrage opportunity found for {gmo_symbol}.")
            else:
                print(f"Could not fetch ticker data for {gmo_symbol} from one or both exchanges.")

        print(f"\nWaiting for {config.FETCH_INTERVAL_SECONDS} seconds before next cycle...")
        time.sleep(config.FETCH_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
