import ccxt
import time
import os

exchange_ids = ['binance', 'kucoin', 'mexc', 'bybit', 'okx']
exchanges = []

for eid in exchange_ids:
    try:
        ex = getattr(ccxt, eid)()
        exchanges.append(ex)
    except Exception as e:
        print(f"Could not initialize {eid}: {e}")

symbol = 'DOGE/USDT'
fee_buffer = 0.002

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    prices = []

    print(f"--- Monitoring {symbol} ---")
    for ex in exchanges:
        try:
            ticker = ex.fetch_ticker(symbol)
            prices.append({
                'name': ex.id,
                'bid': ticker['bid'],
                'ask': ticker['ask']
            })
            print(f"{ex.id:10} | Bid: {ticker['bid']:<10} | Ask: {ticker['ask']:<10}")
        except Exception as e:
            print(f"{ex.id:10} | Error: {e}")

    print("-" * 45)

    if len(prices) > 1:
        best_buy = min(prices, key=lambda x: x['ask'])
        best_sell = max(prices, key=lambda x: x['bid'])
        if best_buy['ask'] < best_sell['bid'] * (1 - fee_buffer):
            profit_pct = ((best_sell['bid'] / best_buy['ask']) - 1) * 100
            print(f"🚀 OPPORTUNITY FOUND!")
            print(f"BUY at  : {best_buy['name'].upper()} ({best_buy['ask']})")
            print(f"SELL at : {best_sell['name'].upper()} ({best_sell['bid']})")
            print(f"PROFIT  : {profit_pct:.4f}%")
        else:
            print("Status: Scanning... No spread wide enough.")
    time.sleep(5)