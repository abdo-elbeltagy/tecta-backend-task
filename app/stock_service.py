import yfinance as yf
import time
def get_stock_data(ticker: str, start: str = None, end: str = None):
    # Fetch historical data
    data = get_price_data(ticker, start=start, end=end)
    if data.empty:
        return None
    # Calculate statistics
    stats = {
        "ticker": ticker,
        "start_date": start,
        "end_date": end,
        "high": data["High"].max(),
        "low": data["Low"].min(),
        "average": data["Close"].mean(),
        "last_close": data["Close"].iloc[-1],
    }
    print(f"Calculated stats: {stats}")
    return stats


# cache dictionary
_cache = {}
CACHE_TTL = 300  # 1 minute

def _make_cache_key(ticker: str, start: str = None, end: str = None):
    return f"{ticker}_{start}_{end}"

def _is_cache_valid(entry):
    return time.time() - entry["timestamp"] < CACHE_TTL

def get_price_data(ticker: str, start: str = None, end: str = None):
    key = _make_cache_key(ticker, start, end)
    
    # check cache
    if key in _cache and _is_cache_valid(_cache[key]):
        print(f"Cache hit for {key}")
        return _cache[key]["data"]

    # fetch fresh data
    data = yf.download(ticker, start=start, end=end)
    print(f"Fetched data for {ticker} from {start} to {end}")
    # store in cache
    _cache[key] = {"data": data, "timestamp": time.time()}
    return data


def calculate_stats(ticker: str, start: str = None, end: str = None):
    data = get_price_data(ticker, start, end)

    if data.empty:
        return {"error": "No data found for ticker"}

    high = data["High"].max()
    low = data["Low"].min()
    avg = data["Close"].mean()
    last_close = data["Close"].iloc[-1]

    return {
        "ticker": ticker,
        "high": high,
        "low": low,
        "average": avg,
        "last_close": last_close
    }