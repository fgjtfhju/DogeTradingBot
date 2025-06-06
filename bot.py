
import time
import logging
import datetime

logging.basicConfig(level=logging.INFO)

def fake_trading_strategy():
    # Simulert strategi
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"[{now}] Simulert handel: Kjøp DOGE, 3x gearing, breakout sjekket.")

while True:
    fake_trading_strategy()
    time.sleep(60)
