import uvicorn
import requests
import yaml
from fastapi import FastAPI
from redis import Redis


with open("config.yml", "r") as f:
    config = yaml.safe_load(f)
    API_BASE_URL = config["api_base_url"]
    DEFAULT_CACHE_TIME = int(config["default_cache_time"])
    DEFAULT_SERVER_PORT = int(config["default_server_port"])
    REDIS_SERVER = config["redis_server"]
    REDIS_PORT = int(config["default_server_port"])

app = FastAPI()
redis = Redis(host=REDIS_SERVER, port=6379)

@app.get("/{crypto}")
async def get_crypto_price(crypto: str):
    price = redis.get(crypto)
    if price is None: # Record is not in the database or its expiry date has passed
        url = f"?ids={crypto}&vs_currencies=usd"

        response = requests.get(API_BASE_URL + url)

        if response.status_code == 200: #HTTP: OK
            response_text = "Name: " + crypto + ", Current Price: " + str(response.json()[crypto]["usd"])
            redis.set(crypto, response.json()[crypto]["usd"], DEFAULT_CACHE_TIME)
            return response_text
        
        else: # Something must have gone wrong
            return "Something went wrong"
    else: # Record is in the data base and is fresh
        response_text = "Name: " + crypto + ", Current Price: " + price.decode() + " (might be outdated for at most 5 mins)"
        return response_text

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=DEFAULT_SERVER_PORT)
