
import time
import logging
import os
from datetime import datetime
from binance.client import Client
from binance.enums import *

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

api_key = os.environ.get("BINANCE_API_KEY")
api_secret = os.environ.get("BINANCE_API_SECRET")

client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'

symbol = os.environ.get("TRADE_SYMBOL", "DOGEUSDT")
quantity = float(os.environ.get("TRADE_QUANTITY", "500"))

def place_order(order_type):
    try:
        if order_type == "BUY":
            order = client.order_market_buy(symbol=symbol, quantity=quantity)
        elif order_type == "SELL":
            order = client.order_market_sell(symbol=symbol, quantity=quantity)
        logging.info(f"{order_type} order placed: {order}")
    except Exception as e:
        logging.error(f"Failed to place {order_type} order: {e}")

def strategy():
    try:
        klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=10)
        close_prices = [float(k[4]) for k in klines]
        last = close_prices[-1]
        min_10 = min(close_prices)
        max_10 = max(close_prices)

        logging.info(f"Aktuell pris: {last:.6f} | Min: {min_10:.6f} | Max: {max_10:.6f}")

        if last > max_10 * 0.995:
            logging.info(f"Breakout signal: Kjøper @ {last}")
            place_order("BUY")
        elif last < min_10 * 1.002:
            logging.info(f"Range-bunn signal: Kjøper @ {last}")
            place_order("BUY")
        elif last > max_10 * 0.9965:
            logging.info(f"Nesten breakout – vurderer kjøp. Pris: {last}")
        else:
            logging.info(f"Ingen handling. Pris: {last}")
    except Exception as e:
        logging.error(f"Strategifeil: {e}")

while True:
    strategy()
    time.sleep(60)
