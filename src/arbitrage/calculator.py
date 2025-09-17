def calculate_arbitrage(gmo_ticker: dict, bitbank_ticker: dict):
    """
    GMOコインとbitbankのティッカー情報から裁定機会を計算します。

    Args:
        gmo_ticker (list): GMOコインのAPIから取得したティッカー情報のリスト。
                           list of dicts, so we take the first element.
        bitbank_ticker (dict): bitbankのAPIから取得したティッカー情報。

    Returns:
        list: 裁定機会を表す辞書のリスト。機会がなければ空のリスト。
    """
    opportunities = []

    if not gmo_ticker or not bitbank_ticker:
        return opportunities

    # GMOのティッカーはリストで返ってくるため、最初の要素を取得
    gmo_ticker_data = gmo_ticker[0]

    # --- Case 1: Buy on GMO Coin, Sell on bitbank ---
    # GMOで買い（ask）、bitbankで売り（buy）
    try:
        gmo_ask = float(gmo_ticker_data['ask'])
        bitbank_buy = float(bitbank_ticker['buy'])

        if gmo_ask < bitbank_buy:
            profit = bitbank_buy - gmo_ask
            profit_rate = (profit / gmo_ask)
            opportunities.append({
                'buy_exchange': 'GMO Coin',
                'sell_exchange': 'bitbank',
                'buy_price': gmo_ask,
                'sell_price': bitbank_buy,
                'profit': profit,
                'profit_rate': profit_rate
            })
    except (ValueError, KeyError) as e:
        print(f"Could not parse ticker data for Case 1: {e}")


    # --- Case 2: Buy on bitbank, Sell on GMO Coin ---
    # bitbankで買い（sell）、GMOで売り（bid）
    try:
        bitbank_sell = float(bitbank_ticker['sell'])
        gmo_bid = float(gmo_ticker_data['bid'])

        if bitbank_sell < gmo_bid:
            profit = gmo_bid - bitbank_sell
            profit_rate = (profit / bitbank_sell)
            opportunities.append({
                'buy_exchange': 'bitbank',
                'sell_exchange': 'GMO Coin',
                'buy_price': bitbank_sell,
                'sell_price': gmo_bid,
                'profit': profit,
                'profit_rate': profit_rate
            })
    except (ValueError, KeyError) as e:
        print(f"Could not parse ticker data for Case 2: {e}")

    return opportunities
