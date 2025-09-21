import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# ルートディレクトリからの相対パス
LOG_FILE_PATH = 'price_log.csv'

@app.route('/')
def index():
    """
    ダッシュボードのメインページを表示します。
    CSVからデータを読み込み、テンプレートに渡します。
    """
    try:
        # CSVファイルを読み込む
        df = pd.read_csv(LOG_FILE_PATH)
        # データを辞書のリストに変換してHTMLで扱いやすくする
        data = df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"Log file not found at {LOG_FILE_PATH}. Displaying empty dashboard.")
        data = []
    except Exception as e:
        print(f"An error occurred while reading the log file: {e}")
        data = []

    # グラフ用のデータを準備する
    chart_data = None
    if not df.empty:
        # タイムスタンプのフォーマットを整える
        df['datetime_utc'] = pd.to_datetime(df['datetime_utc'])
        # 最新100件に絞るなど、データ量を調整することも可能
        df_chart = df.tail(100)

        chart_data = {
            'labels': [d.strftime('%H:%M:%S') for d in df_chart['datetime_utc']],
            'gmo_sell_prices': list(df_chart['gmo_sell']),
            'bitbank_sell_prices': list(df_chart['bitbank_sell']),
        }

    return render_template('index.html', log_data=data, chart_data=chart_data)

if __name__ == '__main__':
    # このファイルが直接実行された場合（開発時など）、
    # Flaskの開発サーバーを起動します。
    # host='0.0.0.0' を指定して、コンテナ外からのアクセスを許可
    app.run(debug=True, host='0.0.0.0', port=8080)
