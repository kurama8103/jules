import pandas as pd

def add_sma(df: pd.DataFrame, period: int) -> pd.DataFrame:
    """
    DataFrameに単純移動平均線(SMA)の列を追加します。

    Args:
        df (pd.DataFrame): 'close'列を含むローソク足データ
        period (int): SMAを計算する期間

    Returns:
        pd.DataFrame: SMAの列が追加されたDataFrame
    """
    column_name = f"SMA_{period}"
    df[column_name] = df['close'].rolling(window=period).mean()
    return df

if __name__ == '__main__':
    # --- Test ---
    # サンプルのDataFrameを作成
    data = {
        'timestamp': pd.to_datetime(['2024-01-01 00:01', '2024-01-01 00:02', '2024-01-01 00:03', '2024-01-01 00:04', '2024-01-01 00:05', '2024-01-01 00:06']),
        'open': [100, 101, 102, 103, 104, 105],
        'high': [100, 101, 102, 103, 104, 105],
        'low': [100, 101, 102, 103, 104, 105],
        'close': [100, 101, 102, 103, 104, 105],
        'volume': [1, 1, 1, 1, 1, 1]
    }
    sample_df = pd.DataFrame(data)

    # 期間5のSMAを計算
    period_to_calc = 5
    df_with_sma = add_sma(sample_df, period_to_calc)

    print(f"--- DataFrame with SMA({period_to_calc}) ---")
    print(df_with_sma)

    # 検算
    # 5番目のSMAは (100+101+102+103+104)/5 = 102.0
    # 6番目のSMAは (101+102+103+104+105)/5 = 103.0
    print("\nExpected SMA at index 4: 102.0")
    print("Expected SMA at index 5: 103.0")
