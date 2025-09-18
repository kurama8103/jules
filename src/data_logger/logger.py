import csv
import os
from datetime import datetime

LOG_FILE = 'price_log.csv'
FIELDNAMES = [
    'timestamp',
    'datetime_utc',
    'symbol',
    'gmo_buy',
    'gmo_sell',
    'bitbank_buy',
    'bitbank_sell'
]

def log_ticker_data(symbol: str, gmo_ticker: list, bitbank_ticker: dict):
    """
    取得したティッカーデータをCSVファイルに追記します。

    Args:
        symbol (str): 通貨シンボル。
        gmo_ticker (list): GMOコインのティッカー情報。
        bitbank_ticker (dict): bitbankのティッカー情報。
    """
    if not gmo_ticker or not bitbank_ticker:
        return

    try:
        gmo_data = gmo_ticker[0]

        log_entry = {
            'timestamp': int(datetime.now().timestamp()),
            'datetime_utc': datetime.utcnow().isoformat(),
            'symbol': symbol,
            'gmo_buy': gmo_data.get('bid'),
            'gmo_sell': gmo_data.get('ask'),
            'bitbank_buy': bitbank_ticker.get('buy'),
            'bitbank_sell': bitbank_ticker.get('sell')
        }

        # ファイルが存在しない場合はヘッダーを書き込む
        file_exists = os.path.isfile(LOG_FILE)

        with open(LOG_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            if not file_exists:
                writer.writeheader()
            writer.writerow(log_entry)

    except (KeyError, IndexError, TypeError) as e:
        print(f"Error preparing log data: {e}")
    except IOError as e:
        print(f"Error writing to log file {LOG_FILE}: {e}")
