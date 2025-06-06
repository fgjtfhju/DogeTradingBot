
import os
import time
import logging
import smtplib
from email.message import EmailMessage
from binance.client import Client
from binance.enums import *

# Logger
logging.basicConfig(filename="doge_trading_log.txt", level=logging.INFO)

# API-nøkler
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET")
client = Client(api_key, api_secret, testnet=True)

symbol = "DOGEUSDT"
leverage = 3
quantity = 150  # ca 3x gearing på 50 USDT
entry_price = None
stop_loss_pct = 0.97  # 3 % ned

# E-postvarsel
def send_email(subject, body):
    try:
        email_address = os.getenv("EMAIL_ADDRESS")
        email_password = os.getenv("EMAIL_PASSWORD")
        recipient = os.getenv("EMAIL_RECIPIENT")

        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = email_address
        msg["To"] = recipient

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
    except Exception as e:
        logging.error(f"E-postfeil: {e}")

def log(msg):
    logging.info(msg)
    print(msg)
    send_email("DogeBot Handel", msg)

def get_price():
    return float(client.get_symbol_ticker(symbol=symbol)["price"])

def place_order(side):
    global entry_price
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        price = get_price()
        entry_price = price if side == SIDE_BUY else None
        log(f"{side} order utført til pris {price}")
    except Exception as e:
        log(f"Order-feil: {e}")

prev_high = get_price()
prev_low = prev_high

log("DogeTradingBot (live) kjører...")

while True:
    try:
        price = get_price()
        log(f"Nåværende pris: {price}")

        # Breakout kjøp
        if price > prev_high * 1.01:
            place_order(SIDE_BUY)
            prev_high = price

        # Range trading salg
        elif price < prev_low * 0.99:
            place_order(SIDE_SELL)
            prev_low = price

        # Stop loss
        if entry_price and price < entry_price * stop_loss_pct:
            place_order(SIDE_SELL)
            log(f"Stop loss aktivert ved {price}")

        time.sleep(60)
    except Exception as e:
        log(f"Feil i hovedsløyfe: {e}")
        time.sleep(60)
