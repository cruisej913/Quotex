import time
from datetime import datetime, timedelta
from telegram import Bot
from tradingview_ta import TA_Handler, Interval, Exchange

# --- CONFIGURATION ---
TOKEN = "8120783279:AAEEJG0KPyTxyqCCRjtilVbwC9-WjI_Y3PU"  # tumhara bot token
CHAT_ID = "1464107392"  # tumhara chat id

bot = Bot(token=TOKEN)

ASSETS = {
    "EUR/USD": "FX_IDC:EURUSD",
    "GBP/USD": "FX_IDC:GBPUSD",
    "USD/JPY": "FX_IDC:USDJPY",
    "USD/CHF": "FX_IDC:USDCHF",
    "BTC/USD": "BINANCE:BTCUSDT",
    "ETH/USD": "BINANCE:ETHUSDT",
    "LTC/USD": "BINANCE:LTCUSDT",
    "SOL/USD": "BINANCE:SOLUSDT",
}

def get_signal(symbol):
    handler = TA_Handler(
        symbol=symbol,
        screener="crypto" if "BINANCE" in symbol else "forex",
        exchange="BINANCE" if "BINANCE" in symbol else "FX_IDC",
        interval=Interval.INTERVAL_15_MINUTES
    )
    analysis = handler.get_analysis()
    return analysis.summary["RECOMMENDATION"]

def send_signal(asset, action, trade_time):
    message = f"""📈 Quotex AI Signal:
🔔 Asset: {asset}
📅 Timeframe: 15 Min
🕐 Trade Time: {trade_time}
📈 Action: {action}
#TRADEGENIOUSBOT"""
    bot.send_message(chat_id=CHAT_ID, text=message)
    print(f"✅ Signal Sent for {asset} ({action}) at {trade_time}")

while True:
    now = datetime.now()
    current_minute = now.minute

    # Run only at every new 15-min block
    if current_minute % 15 == 0:
        for asset, symbol in ASSETS.items():
            try:
                signal = get_signal(symbol)
                if signal == "STRONG_BUY":
                    action = "BUY"
                elif signal == "STRONG_SELL":
                    action = "SELL"
                else:
                    continue  # Skip if no strong signal

                # 5 min future trade time
                trade_time = (now + timedelta(minutes=5)).strftime("%I:%M %p")
                send_signal(asset, action, trade_time)
                time.sleep(2)  # slight delay between assets
            except Exception as e:
                print(f"Error with {asset}: {e}")

        # Wait for 60 seconds to avoid multiple triggers in same candle
        time.sleep(60)
    else:
        print("⌛ Waiting for next 15 min block...")
        time.sleep(10)
