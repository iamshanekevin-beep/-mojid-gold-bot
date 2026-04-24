from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Mojid Gold Bot API running"}

@app.get("/gold-price")
async def gold_price():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(
                "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=XAU&to_currency=USD&apikey=S8ONK8D5MHYWASFF"
            )
            if res.status_code == 200:
                data = res.json()
                rate = data.get("Realtime Currency Exchange Rate", {}).get("5. Exchange Rate")
                if rate:
                    spot = round(float(rate), 2)
                    iq_price = round(spot * 1.4197, 1)
                    return {
                        "spot": spot,
                        "iq_price": iq_price,
                        "source": "Alpha Vantage XAU/USD",
                        "status": "ok"
                    }
    except Exception:
        pass

    return {"status": "error", "message": "All feeds failed"}
