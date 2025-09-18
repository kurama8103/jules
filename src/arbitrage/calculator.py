import config

def calculate_arbitrage(gmo_ticker: list, bitbank_ticker: dict):
    """
    GMOコインとbitbankのティッカー情報から手数料を考慮した裁定機会を計算します。

    Args:
        gmo_ticker (list): GMOコインのAPIから取得したティッカー情報のリスト。
        bitbank_ticker (dict): bitbankのAPIから取得したティッカー情報。

    Returns:
        list: 裁定機会を表す辞書のリスト。機会がなければ空のリスト。
    """
    opportunities = []

    if not gmo_ticker or not bitbank_ticker:
        return opportunities

    gmo_ticker_data = gmo_ticker[0]

    # --- Case 1: Buy on GMO Coin, Sell on bitbank ---
    try:
        buy_price = float(gmo_ticker_data['ask'])
        sell_price = float(bitbank_ticker['buy'])

        # 手数料計算
        buy_fee = buy_price * config.GMO_COIN_FEE_RATE
        sell_fee = sell_price * config.BITBANK_FEE_RATE

        # 純利益
        net_profit = sell_price - buy_price - buy_fee - sell_fee

        if net_profit > 0:
            profit_rate = net_profit / buy_price
            opportunities.append({
                'buy_exchange': 'GMO Coin',
                'sell_exchange': 'bitbank',
                'buy_price': buy_price,
                'sell_price': sell_price,
                'profit': net_profit,
                'profit_rate': profit_rate
            })
    except (ValueError, KeyError) as e:
        print(f"Could not parse ticker data for Case 1: {e}")

    # --- Case 2: Buy on bitbank, Sell on GMO Coin ---
    try:
        buy_price = float(bitbank_ticker['sell'])
        sell_price = float(gmo_ticker_data['bid'])

        # 手数料計算
        buy_fee = buy_price * config.BITBANK_FEE_RATE
        sell_fee = sell_price * config.GMO_COIN_FEE_RATE

        # 純利益
        net_profit = sell_price - buy_price - buy_fee - sell_fee

        if net_profit > 0:
            profit_rate = net_profit / buy_price
            opportunities.append({
                'buy_exchange': 'bitbank',
                'sell_exchange': 'GMO Coin',
                'buy_price': buy_price,
                'sell_price': sell_price,
                'profit': net_profit,
                'profit_rate': profit_rate
            })
    except (ValueError, KeyError) as e:
        print(f"Could not parse ticker data for Case 2: {e}")

    return opportunities
