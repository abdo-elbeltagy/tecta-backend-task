import yfinance as yf
import pandas as pd

def get_stock_data(ticker: str, start: str = None, end: str = None):
    # Fetch historical data
    data = yf.download(ticker, start=start, end=end)
    if data.empty:
        return None
    print(f"Data for {ticker} from {start} to {end}: {data.head()}")
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
