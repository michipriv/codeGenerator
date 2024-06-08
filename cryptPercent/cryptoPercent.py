import os
import sys
from binance.client import Client
import pandas as pd
from datetime import datetime
import json
import pytz
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mplfinance as mpf

# Setze das Backend auf TkAgg
matplotlib.use('TkAgg')

def flush_print(message):
    print(message)
    sys.stdout.flush()

# Wechsel in das Verzeichnis 'cryptPercent'
os.chdir('cryptPercent')

# Lade API-Schlüssel und Geheimnis aus der Datei api_key.json
with open('api_key.json') as f:
    keys = json.load(f)
api_key = keys['api_key']
api_secret = keys['api_secret']

# Initialisiere den Binance-Client
client = Client(api_key, api_secret)

def get_klines(symbol, interval, start_str, end_str=None):
    flush_print(f"Rufe Kerzen für {symbol} von {start_str} bis {end_str} ab")
    klines = client.get_historical_klines(symbol, interval, start_str, end_str)
    flush_print(f"{len(klines)} Kerzen abgerufen")
    return klines

def find_ll_hh(df):
    lowest_low = None
    lowest_low_index = None
    highest_high = None
    highest_high_index = None
    
    for i in range(len(df) - 5):
        # Check for LL
        if df['close'].iloc[i] < df['open'].iloc[i] and df['close'].iloc[i+1] > df['open'].iloc[i+1] and df['close'].iloc[i+2] > df['open'].iloc[i+2] and df['close'].iloc[i+3] > df['open'].iloc[i+3]:
            local_low = df['low'].iloc[i:i+4].min()
            if lowest_low is None or local_low < lowest_low:
                lowest_low = local_low
                lowest_low_index = df.iloc[i:i+4]['low'].idxmin()
        
        # Check for HH
        if df['close'].iloc[i] > df['open'].iloc[i] and df['close'].iloc[i+1] < df['open'].iloc[i+1] and df['close'].iloc[i+2] < df['open'].iloc[i+2]:
            local_high = df['high'].iloc[i:i+3].max()
            if highest_high is None or local_high > highest_high:
                highest_high = local_high
                highest_high_index = df.iloc[i:i+3]['high'].idxmax()

    return lowest_low, lowest_low_index, highest_high, highest_high_index

def plot_candlestick_chart(df):
    mc = mpf.make_marketcolors(up='g', down='r', inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc)

    # Konvertiere die UTC-Zeit in Wiener Zeit (UTC+2)
    df.index = df.index.tz_localize('UTC').tz_convert('Europe/Vienna')

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting the candlestick chart using mplfinance
    mpf.plot(df, type='candle', style=s, ax=ax)

    # Berechne die Gesamtdauer in Stunden
    total_hours = (df.index[-1] - df.index[0]).total_seconds() / 3600

    # Hartkodiert: maximal 10 Hauptintervalle
    major_interval = max(1, int(total_hours / 10))

    # Setting the x-axis major locator to display dates
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=major_interval))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n%d.%m.%y'))

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, fontsize=10)

    # Keine Minor-Ticks setzen
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=major_interval))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter(''))

    # Adjust the limits of the x-axis
    ax.set_xlim([df.index[0], df.index[-1]])

    # Display the plot
    plt.show()

def main(symbol, start_date, end_date=None):
    flush_print(f"Starte Analyse für {symbol} von {start_date} bis {end_date}")
    interval = Client.KLINE_INTERVAL_15MINUTE
    
    # Holen Sie sich die Kerzendaten von Binance
    klines = get_klines(symbol, interval, start_date, end_date)
    
    # Trim the data to only include the required fields
    data = [item[:6] for item in klines]
    
    # Convert data to appropriate types
    df = pd.DataFrame(data, columns=['open_time', 'open', 'high', 'low', 'close', 'volume'])
    df = df.astype({
        'open': 'float',
        'high': 'float',
        'low': 'float',
        'close': 'float',
        'volume': 'float'
    })
    
    df['Date'] = pd.to_datetime(df['open_time'], unit='ms')
    df.set_index('Date', inplace=True)
    
    # Find LL and HH
    lowest_low, lowest_low_index, highest_high, highest_high_index = find_ll_hh(df)
    
    # Ergebnisse ausgeben
    flush_print("Ergebnisse:")
    flush_print(f"Lowest Low (LL): {lowest_low} at index {lowest_low_index}")
    flush_print(f"Highest High (HH): {highest_high} at index {highest_high_index}")
    
    # Grafik anzeigen
    plot_candlestick_chart(df)

# Beispielaufruf
if __name__ == "__main__":
    symbol = "SEIUSDT"  # Handelspaar für SEI
    start_date = "1 day ago UTC"
    
    main(symbol, start_date)