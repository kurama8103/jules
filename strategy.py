import pandas as pd
import config

def check_cross(df: pd.DataFrame) -> str:
    """
    DataFrameの最新データからゴールデンクロス/デッドクロスを判定します。

    Args:
        df (pd.DataFrame): 短期・長期のSMA列を含むデータフレーム。
                           列名は config.py の設定に基づきます (例: 'SMA_5', 'SMA_25')

    Returns:
        str: 'buy', 'sell', 'hold' のいずれかを返す
    """
    short_sma_col = f"SMA_{config.SHORT_SMA_PERIOD}"
    long_sma_col = f"SMA_{config.LONG_SMA_PERIOD}"

    # 必要なSMA列が存在するかチェック
    if short_sma_col not in df.columns or long_sma_col not in df.columns:
        return 'hold'

    # 計算に必要なデータ（最低2行）があるかチェック
    if len(df) < 2:
        return 'hold'

    # 最新の2つのデータを取得
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    # SMAの値が計算されているか（NaNでないか）チェック
    if pd.isna(last_row[short_sma_col]) or pd.isna(last_row[long_sma_col]) or \
       pd.isna(prev_row[short_sma_col]) or pd.isna(prev_row[long_sma_col]):
        return 'hold'

    # ゴールデンクロス判定
    # (前回) 短期SMA < 長期SMA  AND  (今回) 短期SMA > 長期SMA
    if prev_row[short_sma_col] < prev_row[long_sma_col] and \
       last_row[short_sma_col] > last_row[long_sma_col]:
        return 'buy'

    # デッドクロス判定
    # (前回) 短期SMA > 長期SMA  AND  (今回) 短期SMA < 長期SMA
    if prev_row[short_sma_col] > prev_row[long_sma_col] and \
       last_row[short_sma_col] < last_row[long_sma_col]:
        return 'sell'

    return 'hold'

if __name__ == '__main__':
    # --- Test ---
    short_col = f"SMA_{config.SHORT_SMA_PERIOD}"
    long_col = f"SMA_{config.LONG_SMA_PERIOD}"

    # 1. ゴールデンクロスのテストデータ
    gc_data = {
        short_col: [100, 110],
        long_col: [105, 105]
    }
    df_gc = pd.DataFrame(gc_data)
    print(f"Testing Golden Cross... Expected: buy, Got: {check_cross(df_gc)}")

    # 2. デッドクロスのテストデータ
    dc_data = {
        short_col: [110, 100],
        long_col: [105, 105]
    }
    df_dc = pd.DataFrame(dc_data)
    print(f"Testing Dead Cross...   Expected: sell, Got: {check_cross(df_dc)}")

    # 3. 何も起きない（ホールド）のテストデータ
    hold_data = {
        short_col: [110, 115],
        long_col: [105, 105]
    }
    df_hold = pd.DataFrame(hold_data)
    print(f"Testing Hold...         Expected: hold, Got: {check_cross(df_hold)}")

    # 4. データが足りない場合のテスト
    not_enough_data = {
        short_col: [110],
        long_col: [105]
    }
    df_ne = pd.DataFrame(not_enough_data)
    print(f"Testing Not Enough Data... Expected: hold, Got: {check_cross(df_ne)}")

    # 5. NaNが含まれる場合のテスト
    nan_data = {
        short_col: [None, 110],
        long_col: [105, 105]
    }
    df_nan = pd.DataFrame(nan_data)
    print(f"Testing NaN Data...     Expected: hold, Got: {check_cross(df_nan)}")
