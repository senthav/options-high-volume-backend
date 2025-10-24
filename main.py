from fastapi import FastAPI, Query
import yfinance as yf
import pandas as pd

app = FastAPI(title="Options High Volume Finder")

@app.get("/options")
def get_high_volume_options(symbol: str = Query(...), expiration: str = Query(...)):
    """
    Returns options with high volume for a given stock and expiration date.
    """
    try:
        stock = yf.Ticker(symbol)
        options_chain = stock.option_chain(expiration)
        calls = options_chain.calls
        puts = options_chain.puts

        # Get top 5 by volume
        top_calls = calls.sort_values(by="volume", ascending=False).head(5)
        top_puts = puts.sort_values(by="volume", ascending=False).head(5)

        return {
            "symbol": symbol,
            "expiration": expiration,
            "top_calls": top_calls.to_dict(orient="records"),
            "top_puts": top_puts.to_dict(orient="records")
        }
    except Exception as e:
        return {"error": str(e)}
