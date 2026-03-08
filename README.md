# 🔄 Crypto Arbitrage Scanner  (Arbitrex)
A real‑time arbitrage scanner that monitors multiple crypto exchanges using **CCXT**.

## 📌 Overview  
This script continuously tracks the price of a selected trading pair (e.g., `DOGE/USDT`) across several exchanges and automatically detects arbitrage opportunities by comparing **bid** and **ask** prices. A configurable buffer helps account for trading fees and slippage.

Every 5 seconds the script:
- Fetches prices from Binance, KuCoin, MEXC, Bybit, and OKX  
- Displays bid/ask values in real time  
- Identifies the best exchange to buy and the best to sell  
- Calculates potential profit percentage  
- Highlights any arbitrage opportunity 🚀  

---

## 🧩 Key Features
- Real‑time price monitoring  
- Multi‑exchange support  
- Automatic spread calculation  
- Arbitrage opportunity detection  
- Clean and readable terminal output  

---

## 🛠️ Requirements
Make sure you have:

- **Python 3.8+**
- **CCXT library**

Install CCXT with:

```bash
pip install ccxt
```

---

## ▶️ How to Run

Execute the script:

```bash
python arbitrage.py
```

Example output:

```
--- Monitoring DOGE/USDT ---
binance    | Bid: 0.1234     | Ask: 0.1235
kucoin     | Bid: 0.1233     | Ask: 0.1236
mexc       | Bid: 0.1232     | Ask: 0.1237
---------------------------------------------
Status: Scanning... No spread wide enough.
```

When an opportunity appears:

```
🚀 OPPORTUNITY FOUND!
BUY at  : BINANCE (0.1235)
SELL at : KUCOIN (0.1241)
PROFIT  : 0.4862%
```

---

## ⚙️ Configuration

### Trading pair
```python
symbol = 'DOGE/USDT'
```

### Exchanges to monitor
```python
exchange_ids = ['binance', 'kucoin', 'mexc', 'bybit', 'okx']
```

### Fee/slippage buffer
```python
fee_buffer = 0.002  # 0.2%
```

---

## 📄 Full Source Code

```python
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
```

---

## ⚠️ Disclaimer  
This script is for educational purposes only.  
Real arbitrage involves risks: fees, slippage, transfer delays, API limits, and liquidity can eliminate theoretical profit.
