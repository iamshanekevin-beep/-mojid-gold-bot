from fastapi import FastAPI
from fastapi.middleware.cors import from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = {"price": None, "timestamp": 0}
CACHE_TTL = 300

KEYS = ["S8ONK8D5MHYWASFF", "MNY89MM20RNPM8PI"]
key_index = {"i": 0}

BOT_TOKEN = "8608644762:AAHzFLeUx9BjUjyIXFPL5bY-zFk4NEO_elk"
CHAT_ID = "6758027951"

@app.get("/")
def root():
    return {"status": "Mojid Gold Bot API running"}

@app.get("/gold-price")
async def gold_price():
    now = time.time()
    if cache["price"] and (now - cache["timestamp"]) < CACHE_TTL:
        data = cache["price"].copy()
        data["cached"] = True
        return data
    for _ in range(len(KEYS)):
        key = KEYS[key_index["i"] % len(KEYS)]
        key_index["i"] += 1
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(
                    f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=XAU&to_currency=USD&apikey={key}"
                )
                if res.status_code == 200:
                    data = res.json()
                    rate = data.get("Realtime Currency Exchange Rate", {}).get("5. Exchange Rate")
                    if rate:
                        spot = round(float(rate), 2)
                        iq_price = round(spot * 1.4197, 1)
                        result = {
                            "spot": spot,
                            "iq_price": iq_price,
                            "source": "Alpha Vantage XAU/USD",
                            "status": "ok",
                            "cached": False
                        }
                        cache["price"] = result.copy()
                        cache["timestamp"] = now
                        return result
        except Exception:
            pass
    if cache["price"]:
        data = cache["price"].copy()
        data["cached"] = True
        data["stale"] = True
        return data
    return {"status": "error", "message": "All feeds failed"}

@app.post("/send-signal")
async def send_signal(payload: dict):
    text = payload.get("text", "")
    if not text:
        return {"status": "error", "message": "No text provided"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": CHAT_ID,
                    "text": text,
                    "parse_mode": "HTML"
                }
            )
            data = res.json()
            if data.get("ok"):
                return {"status": "ok", "message": "Signal sent to Telegram"}
            else:
                return {"status": "error", "message": data.get("description", "Unknown error")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

import httpx
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = {"price": None, "timestamp": 0}
CACHE_TTL = 300

KEYS = ["S8ONK8D5MHYWASFF", "MNY89MM20RNPM8PI"]
key_index = {"i": 0}

BOT_TOKEN = "8608644762:AAHzFLeUx9BjUjyIXFPL5bY-zFk4NEO_elk"
CHAT_ID = "6758027951"

@app.get("/")
def root():
    return {"status": "Mojid Gold Bot API running"}

@app.get("/gold-price")
async def gold_price():
    now = time.time()
    if cache["price"] and (now - cache["timestamp"]) < CACHE_TTL:
        data = cache["price"].copy()
        data["cached"] = True
        return data
    for _ in range(len(KEYS)):
        key = KEYS[key_index["i"] % len(KEYS)]
        key_index["i"] += 1
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(
                    f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=XAU&to_currency=USD&apikey={key}"
                )
                if res.status_code == 200:
                    data = res.json()
                    rate = data.get("Realtime Currency Exchange Rate", {}).get("5. Exchange Rate")
                    if rate:
                        spot = round(float(rate), 2)
                        iq_price = round(spot * 1.4197, 1)
                        result = {
                            "spot": spot,
                            "iq_price": iq_price,
                            "source": "Alpha Vantage XAU/USD",
                            "status": "ok",
                            "cached": False
                        }
                        cache["price"] = result.copy()
                        cache["timestamp"] = now
                        return result
        except Exception:
            pass
    if cache["price"]:
        data = cache["price"].copy()
        data["cached"] = True
        data["stale"] = True
        return data
    return {"status": "error", "message": "All feeds failed"}

@app.post("/send-signal")
async def send_signal(payload: dict):
    text = payload.get("text", "")
    if not text:
        return {"status": "error", "message": "No text provided"}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": CHAT_ID,
                    "text": text,
                    "parse_mode": "HTML"
                }
            )
            data = res.json()
            if data.get("ok"):
                return {"status": "ok", "message": "Signal sent to Telegram"}
            else:
                return {"status": "error", "message": data.get("description", "Unknown error")}
    except Exception as e:
        return {"status": "error", "message": str(e)}
