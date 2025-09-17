import time
from src.gmo_coin import api_client as gmo_client
from src.bitbank import api_client as bitbank_client
from src.arbitrage import calculator
import config

def main():
    """
    メイン処理。
    定期的に各取引所の価格を取得し、裁定機会を計算して表示します。
    """
    print("Starting arbitrage bot...")

    # bitbankのシンボル名は小文字アンダースコア区切り
    bitbank_symbol = config.TARGET_SYMBOL.lower()
    # GMOのシンボル名は単語の間にアンダースコア
    gmo_symbol = config.TARGET_SYMBOL

    while True:
        print(f"--- Fetching data at {time.ctime()} ---")

        # データ取得
        gmo_ticker = gmo_client.get_ticker(gmo_symbol)
        bitbank_ticker = bitbank_client.get_ticker(bitbank_symbol)

        if gmo_ticker and bitbank_ticker:
            # 裁定計算
            opportunities = calculator.calculate_arbitrage(gmo_ticker, bitbank_ticker)

            if opportunities:
                print("Arbitrage opportunities found!")
                for opp in opportunities:
                    print(f"  Buy at {opp['buy_exchange']} for {opp['buy_price']:.2f}")
                    print(f"  Sell at {opp['sell_exchange']} for {opp['sell_price']:.2f}")
                    print(f"  Profit: {opp['profit']:.2f} JPY")
                    print(f"  Profit Rate: {opp['profit_rate']:.4%}")
            else:
                print("No arbitrage opportunity found.")
        else:
            print("Could not fetch ticker data from one or both exchanges.")

        print("\nWaiting for next cycle...")
        time.sleep(10) # 10秒待機

if __name__ == "__main__":
    main()
