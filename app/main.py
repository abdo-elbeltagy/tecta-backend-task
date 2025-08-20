from fastapi import FastAPI, HTTPException, Query
from app.stock_service import get_stock_data

app = FastAPI(title="Tecta Stock API")

@app.get("/api/stats")
def stock_stats(ticker: str = Query(..., description="Ticker symbol, e.g., MSFT"),
                start: str = Query(None, description="Start date YYYY-MM-DD"),
                end: str = Query(None, description="End date YYYY-MM-DD")):
    stats = get_stock_data(ticker, start, end)
    print(f"Retrieved stats: {stats}")
    if not stats:
        raise HTTPException(status_code=404, detail="Stock data not found")
    
    return stats
