import requests
import pandas as pd
from datetime import datetime
import config

def get_candlestick(pair: str, candle_type: str, date_str: str) -> pd.DataFrame:
    """
    bitbank APIからローソク足データを取得します。

    Args:
        pair (str): 通貨ペア (例: 'btc_jpy')
        candle_type (str): ローソク足の種類 (例: '1min')
        date_str (str): 日付 (YYYYMMDD形式)

    Returns:
        pd.DataFrame: ローソク足データ。カラムは ['open', 'high', 'low', 'close', 'volume', 'timestamp']
    """
    api_endpoint = f"{config.API_URL}/{pair}/candlestick/{candle_type}/{date_str}"

    try:
        response = requests.get(api_endpoint, timeout=15) # 15秒のタイムアウトを設定
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる

        data = response.json()

        if data['success'] == 1:
            candlestick_data = data['data']['candlestick'][0]['ohlcv']
            df = pd.DataFrame(candlestick_data, columns=['open', 'high', 'low', 'close', 'volume', 'timestamp'])

            # データ型を適切な型に変換
            df['open'] = df['open'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['close'] = df['close'].astype(float)
            df['volume'] = df['volume'].astype(float)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

            return df
        else:
            print(f"Error from bitbank API: {data.get('data', {}).get('code')}")
            return pd.DataFrame() # 空のDataFrameを返す

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during API request: {e}")
        return pd.DataFrame() # 空のDataFrameを返す

if __name__ == '__main__':
    # --- Test ---
    # 今日の日付をYYYYMMDD形式で取得
    today = datetime.now().strftime('%Y%m%d')

    # BTC/JPYの1分足データを取得してみる
    df_btc_jpy = get_candlestick(config.PAIR, config.CANDLE_TYPE, today)

    if not df_btc_jpy.empty:
        print("Successfully fetched candlestick data:")
        print(df_btc_jpy.head()) # 最初の5件を表示
        print(df_btc_jpy.tail()) # 最後の5件を表示
    else:
        print("Failed to fetch candlestick data.")
