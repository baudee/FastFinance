from fastapi import FastAPI, HTTPException
import yfinance as yf


app = FastAPI()


def get_ticker_info(ticker_symbol: str):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        if not info or not info.get("regularMarketPrice"):
            raise Exception("Ticker not found")
        return info
    except Exception:
        raise HTTPException(
            status_code=404, detail=f"Ticker not found: {ticker_symbol}"
        )


@app.get("/ticker/search")
def search(symbol: str, limit: int = 10):
    data = yf.Search(symbol, max_results=limit)
    return data.quotes


@app.get("/ticker/{symbol}")
def details(symbol: str):
    return get_ticker_info(symbol)


@app.get("/currency/{from_currency}/{to_currency}")
def currency(from_currency: str, to_currency: str):
    symbol = f"{from_currency.upper()}{to_currency.upper()}=X"
    return get_ticker_info(symbol).get("regularMarketPrice")
