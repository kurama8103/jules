import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

PRICE_LOG_FILE_PATH = 'price_log.csv'
OPP_LOG_FILE_PATH = 'opportunities_log.csv'

@app.route('/')
def index():
    """
    ダッシュボードのメインページを表示します。
    CSVからデータを読み込み、選択されたシンボルに基づいてフィルタリングし、
    テンプレートに渡します。
    """
    selected_symbol = request.args.get('symbol', '')

    # --- 価格ログの読み込み ---
    try:
        df_price = pd.read_csv(PRICE_LOG_FILE_PATH)
        all_symbols = sorted(df_price['symbol'].unique())

        if not selected_symbol and all_symbols:
            selected_symbol = all_symbols[0]

        if selected_symbol:
            df_filtered = df_price[df_price['symbol'] == selected_symbol].copy()
        else:
            df_filtered = pd.DataFrame()

        price_data = df_filtered.to_dict(orient='records')

    except (FileNotFoundError, KeyError):
        df_filtered = pd.DataFrame()
        all_symbols = []
        price_data = []

    # --- 裁定機会ログの読み込み ---
    try:
        df_opp = pd.read_csv(OPP_LOG_FILE_PATH)
        if selected_symbol:
            opp_data = df_opp[df_opp['symbol'] == selected_symbol].to_dict(orient='records')
        else:
            opp_data = df_opp.to_dict(orient='records')
    except (FileNotFoundError, KeyError):
        opp_data = []


    # --- グラフ用のデータ準備 ---
    chart_data = None
    if not df_filtered.empty:
        df_filtered['datetime_utc'] = pd.to_datetime(df_filtered['datetime_utc'])
        df_chart = df_filtered.tail(100)

        chart_data = {
            'labels': [d.strftime('%H:%M:%S') for d in df_chart['datetime_utc']],
            'gmo_sell_prices': list(df_chart['gmo_sell']),
            'bitbank_sell_prices': list(df_chart['bitbank_sell']),
        }

    return render_template(
        'index.html',
        price_log_data=price_data,
        opp_log_data=opp_data,
        chart_data=chart_data,
        all_symbols=all_symbols,
        selected_symbol=selected_symbol
    )

if __name__ == '__main__':
    # このファイルが直接実行された場合（開発時など）、
    # Flaskの開発サーバーを起動します。
    # host='0.0.0.0' を指定して、コンテナ外からのアクセスを許可
    app.run(debug=True, host='0.0.0.0', port=8080)
