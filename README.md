# Crypto Arbitrage Bot for GMO Coin & bitbank

This is a simple bot to find cryptocurrency arbitrage opportunities between the GMO Coin and bitbank exchanges.

The bot fetches ticker prices from both exchanges, calculates potential net profit after considering taker fees, and displays any profitable opportunities.

## Project Structure

```
.
├── .gitignore
├── config.py
├── main.py
├── README.md
├── requirements.txt
└── src
    ├── arbitrage
    │   └── calculator.py
    ├── bitbank
    │   └── api_client.py
    └── gmo_coin
        └── api_client.py
```

-   `main.py`: The main script to run the bot.
-   `config.py`: Configuration file for API keys, target symbols, and fees. **(Remember to keep this file private)**
-   `requirements.txt`: A list of Python dependencies.
-   `src/`: Contains all the source code.
    -   `gmo_coin/api_client.py`: Fetches data from the GMO Coin API.
    -   `bitbank/api_client.py`: Fetches data from the bitbank API.
    -   `arbitrage/calculator.py`: Calculates arbitrage opportunities.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Configuration

1.  **Create your configuration file:**
    Rename `config.py.example` to `config.py`.
    ```bash
    cp config.py.example config.py
    ```
    The `config.py` file is listed in `.gitignore` to prevent you from accidentally committing your secret keys.

2.  **Edit `config.py`:**
    Open the newly created `config.py` file and edit the settings.

    *   **API Keys (Optional):** Add your keys if you plan to extend the bot for trading.
    *   **Target Symbols:** Modify the `TARGET_SYMBOLS` list to include the trading pairs you want to monitor.
        ```python
        TARGET_SYMBOLS = ["BTC_JPY", "ETH_JPY", "XRP_JPY"] # Example
        ```
    Note: The symbol format must be `BASE_QUOTE` (e.g., `BTC_JPY`). The script will adapt it for each exchange's specific format (e.g., `btc_jpy` for bitbank).

4.  **Verify Fee Rates:**
    The default taker fees are set in the config. Please verify them against the latest official fee schedules from each exchange.
    ```python
    GMO_COIN_FEE_RATE = 0.0005  # 0.05%
    BITBANK_FEE_RATE = 0.0012   # 0.12%
    ```

## Running the Bot

To start the bot, run the following command from the project's root directory:

```bash
python3 main.py
```

The bot will start fetching prices and printing any arbitrage opportunities it finds every 10 seconds.
