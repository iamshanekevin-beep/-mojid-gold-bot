from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
CORSMiddleware,
allow_origins=[”*”],
allow_methods=[”*”],
allow_headers=[”*”],
)

@app.get(”/”)
def root():
return {“status”: “Mojid Gold Bot API running”}

@app.get(”/gold-price”)
async def gold_price():
# Binance PAXG/USDT — no API key needed
try:
async with httpx.AsyncClient(timeout=5) as client:
res = await client.get(“https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT”)
if res.status_code == 200:
spot = float(res.json()[“price”])
return {
“spot”: round(spot, 2),
“iq_price”: round(spot * 1.4197, 1),
“source”: “Binance”,
“status”: “ok”
}
except Exception:
pass

```
# Fallback — CoinGecko
try:
    async with httpx.AsyncClient(timeout=5) as client:
        res = await client.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=pax-gold&vs_currencies=usd"
        )
        if res.status_code == 200:
            spot = float(res.json()["pax-gold"]["usd"])
            return {
                "spot": round(spot, 2),
                "iq_price": round(spot * 1.4197, 1),
                "source": "CoinGecko",
                "status": "ok"
            }
except Exception:
    pass

return {"status": "error", "message": "All feeds failed"}
```
