import requests
import json

API_URL = "https://public.bitbank.cc"

def get_ticker(pair: str):
    """
    bitbankのPublic APIから指定したペアのティッカー情報を取得します。

    Args:
        pair (str): 通貨ペア (例: "btc_jpy")

    Returns:
        dict: APIからのレスポンス(JSON)を辞書に変換したもの。
              エラー時はNoneを返します。
    """
    endpoint = f"/{pair}/ticker"
    url = API_URL + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        data = response.json()
        if data.get("success") == 1:
            return data.get("data")
        else:
            # bitbankのエラーコードはdataフィールド内にある
            error_code = data.get("data", {}).get("code")
            print(f"Error from bitbank API. Code: {error_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with bitbank API request: {e}")
        return None
    except json.JSONDecodeError:
        print("Failed to decode JSON from bitbank API response.")
        return None
