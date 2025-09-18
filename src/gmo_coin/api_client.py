import requests
import json

API_URL = "https://api.coin.z.com/public"

def get_ticker(symbol: str):
    """
    GMOコインのPublic APIから指定したシンボルのティッカー情報を取得します。

    Args:
        symbol (str): 通貨シンボル (例: "BTC_JPY")

    Returns:
        dict: APIからのレスポンス(JSON)を辞書に変換したもの。
              エラー時はNoneを返します。
    """
    endpoint = f"/v1/ticker?symbol={symbol}"
    url = API_URL + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        data = response.json()
        if data.get("status") == 0:
            return data.get("data", [])
        else:
            print(f"Error from GMO Coin API: {data.get('messages')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with GMO Coin API request: {e}")
        return None
    except json.JSONDecodeError:
        print("Failed to decode JSON from GMO Coin API response.")
        return None
