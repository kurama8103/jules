# -- API settings --
API_URL = "https://public.bitbank.cc"

# -- Trading settings --
PAIR = "btc_jpy"
CANDLE_TYPE = "1min" # Type of candlestick (e.g., 1min, 5min, 1hour, 1day)

# -- Strategy settings --
SHORT_SMA_PERIOD = 5  # Period for the short-term Simple Moving Average
LONG_SMA_PERIOD = 25   # Period for the long-term Simple Moving Average

# -- Execution settings --
INTERVAL_SECONDS = 60 # Interval to fetch data and check for signals (in seconds)
