# Cryptocurrency Arbitrage Monitoring Bot

## 概要 (Overview)

This is a sample Python bot that monitors cryptocurrency prices across three Japanese exchanges—**bitFlyer**, **bitbank**, and **GMO Coin**—to detect arbitrage opportunities.

The bot continuously fetches the latest ticker prices for a specified currency pair (default: `BTC/JPY`) and calculates the potential profit from buying on the cheapest exchange and selling on the most expensive one.

**重要 (Important):** このbotは教育目的のサンプルです。価格差をコンソールに表示するだけで、**実際の取引注文は行いません。**
(This bot is a sample for educational purposes. It only prints price differences to the console and **does not execute any actual trades.**)

## 機能 (Features)

-   Fetches public ticker data from bitFlyer, bitbank, and GMO Coin.
-   Identifies the lowest ask price (best buy price) and highest bid price (best sell price) across the exchanges.
-   Calculates the potential profit from an arbitrage trade.
-   Prints a prominent alert to the console if the potential profit exceeds a configurable threshold.
-   Continuously monitors prices at a configurable interval.

## 必要なもの (Requirements)

-   Python 3.7+

## セットアップ手順 (Setup)

1.  **Clone or download the project files.**

2.  **Install the necessary Python library.**
    This project uses the `ccxt` library to connect to most exchanges. The `requests` library (for GMO Coin) is included as a dependency.

    ```bash
    pip install ccxt
    ```

## 設定方法 (Configuration)

You can configure the bot by editing the variables in the "Configuration" section at the top of the `main.py` file:

-   `SYMBOL_CCXT`: The currency pair symbol for exchanges supported by `ccxt` (e.g., `'BTC/JPY'`).
-   `SYMBOL_GMO`: The currency pair symbol for GMO Coin (e.g., `'BTC_JPY'`).
-   `PROFIT_THRESHOLD`: The minimum potential profit in JPY required to trigger a detailed alert.
-   `REFRESH_INTERVAL_SECONDS`: The number of seconds to wait between each price check.

## 実行方法 (How to Run)

Navigate to the project directory and run the following command:

```bash
python main.py
```

The bot will start fetching prices and displaying the results. To stop the bot, press `Ctrl+C`.

## 免責事項 (Disclaimer)

-   This software is a sample provided for educational purposes only.
-   It does not guarantee any profit and the authors are not responsible for any losses incurred from its use.
-   **This bot does not perform any real trading.** To execute trades, you would need to extend it using the private APIs of the exchanges, which requires handling API keys and implementing order logic. This is a significant and high-risk task.
