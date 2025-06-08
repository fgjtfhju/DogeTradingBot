
import time
import logging
from datetime import datetime
from binance.client import Client
from binance.enums import *

import os

# Logger
logging.basicConfig(level=logging.INFO)

# Miljøvariabler (API-nøkler)
api_key = os.environ.get("BINANCE_API_KEY")
api_secret = os.environ.get("BINANCE_API_SECRET")

client = Client(api_key, api_secret)

symbol = "DOGEUSDT"
quantity = 150  # Justert for 3x gearing – tilpasses kontoverdi

def get_price():
    return float(client.get_symbol_ticker(symbol=symbol)["price"])

def log(msg):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[{t}] {msg}")

log("🚀 Bot startet")

last_price = get_price()
high = last_price
low = last_price

while True:
    try:
        price = get_price()
        log(f"Pris: {price}")

        if price > high * 1.01:
            log("Breakout! Kjøper DOGE (simulert)")
            high = price

        elif price < low * 0.99:
            log("Pris faller! Stop loss eller salg (simulert)")
            low = price

        else:
            log("Ingen handling. Overvåker markedet.")

        
        time.sleep(60)

    except Exception as e:
        log(f"Feil: {e}")
        time.sleep(60)
