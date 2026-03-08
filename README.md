# 🔄 Crypto Arbitrage Scanner  (Arbitrex)
Scanner in tempo reale per individuare opportunità di arbitraggio su più exchange utilizzando **CCXT**.

## 📌 Descrizione  
Questo script monitora il prezzo di una specifica coppia crypto (es. `DOGE/USDT`) su diversi exchange e rileva automaticamente eventuali opportunità di arbitraggio, confrontando **bid** e **ask** e applicando un buffer per coprire le fee.

Ogni 5 secondi:
- Recupera i prezzi da Binance, KuCoin, MEXC, Bybit e OKX  
- Mostra bid/ask in tempo reale  
- Identifica la miglior piattaforma per comprare e quella per vendere  
- Calcola il potenziale profitto percentuale  
- Evidenzia eventuali opportunità 🚀  

---

## 🧩 Funzionalità principali
- Monitoraggio continuo dei prezzi tramite CCXT  
- Supporto multi-exchange  
- Calcolo automatico dello spread  
- Rilevamento opportunità di arbitraggio  
- Output pulito e leggibile in console  

---

## 🛠️ Requisiti
Assicurati di avere installato:

- **Python 3.8+**
- **CCXT**

Installa CCXT con:

```bash
pip install ccxt
```

---

## ▶️ Utilizzo

Esegui lo script:

```bash
python arbitrage.py
```

Il terminale mostrerà qualcosa come:

```
--- Monitoring DOGE/USDT ---
binance    | Bid: 0.1234     | Ask: 0.1235
kucoin     | Bid: 0.1233     | Ask: 0.1236
mexc       | Bid: 0.1232     | Ask: 0.1237
---------------------------------------------
Status: Scanning... No spread wide enough.
```

Quando si presenta un’opportunità:

```
🚀 OPPORTUNITY FOUND!
BUY at  : BINANCE (0.1235)
SELL at : KUCOIN (0.1241)
PROFIT  : 0.4862%
```

---

## ⚙️ Configurazione

Puoi modificare:

### Coppia da monitorare
```python
symbol = 'DOGE/USDT'
```

### Lista degli exchange
```python
exchange_ids = ['binance', 'kucoin', 'mexc', 'bybit', 'okx']
```

### Margine di sicurezza per fee e slippage
```python
fee_buffer = 0.002  # 0.2%
```

---

## 📄 Codice completo

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
Questo script è solo a scopo educativo.  
L’arbitraggio comporta rischi reali: fee, slippage, tempi di trasferimento, limiti API e liquidità possono annullare il profitto teorico.
