import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv
from stable_baselines3 import PPO
from env import AssetAllocationRealEnv

load_dotenv()
API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

def fetch_historical_data(symbol, start, end):
    url = f"https://{API_HOST}/api/yahoo/hi/history/{symbol}/1d"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": API_HOST}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            df = pd.DataFrame(data["items"])
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
            df = df.sort_index()
            df = df[(df.index >= start) & (df.index <= end)]
            return df
    return None

def run_backtest(start_date, end_date):
    btc_df = fetch_historical_data("BTC-USD", start_date, end_date)
    eth_df = fetch_historical_data("ETH-USD", start_date, end_date)
    if btc_df is None or eth_df is None:
        return {"error": "Failed to fetch data"}

    btc_returns = btc_df["close"].pct_change().fillna(0)
    eth_returns = eth_df["close"].pct_change().fillna(0)
    dates = btc_df.index
    df = pd.DataFrame({
        "return_cash": np.zeros_like(btc_returns),
        "return_btc": btc_returns,
        "return_eth": eth_returns
    }, index=dates)

    model = PPO.load("models/ppo_sentiment_model.zip")
    env = AssetAllocationRealEnv(df)
    obs = env.reset()
    done = False
    portfolio_value = 100
    values = [portfolio_value]
    allocations = []

    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        weights = action / (np.sum(action) + 1e-6)
        portfolio_value *= (1 + np.dot(weights, obs))
        values.append(portfolio_value)
        allocations.append([round(w * 100, 2) for w in weights])

    return {
        "final_value": round(values[-1], 2),
        "allocations": allocations
    }