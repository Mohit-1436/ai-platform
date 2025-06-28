from stable_baselines3 import PPO
import numpy as np
from sentiment import get_sentiment

# Load PPO model once
ppo_model = PPO.load("models/ppo_sentiment_model.zip")

def predict_allocation(text, avg_return, cluster):
    sentiment_score = get_sentiment(text)["Score"]
    obs = np.array([avg_return / 100, sentiment_score, cluster], dtype=np.float32)
    action, _ = ppo_model.predict(obs)
    action = action / (np.sum(action) + 1e-6)
    return {
        "sentiment_score": sentiment_score,
        "allocation": {
            "Cash": round(float(action[0]) * 100, 2),
            "BTC": round(float(action[1]) * 100, 2),
            "ETH": round(float(action[2]) * 100, 2)
        }
    }