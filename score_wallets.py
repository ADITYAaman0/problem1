import json
from collections import defaultdict, Counter
import pandas as pd
import numpy as np

INPUT_FILE = "user-wallet-transactions.json"
OUTPUT_FILE = "wallet_scores.csv"

# Load data
with open(INPUT_FILE, "r") as f:
    data = json.load(f)

wallet_features = defaultdict(lambda: Counter({
    'deposit_count': 0,
    'deposit_usd': 0.0,
    'borrow_count': 0,
    'borrow_usd': 0.0,
    'repay_count': 0,
    'repay_usd': 0.0,
    'redeem_count': 0,
    'redeem_usd': 0.0,
    'liquidation_count': 0,
}))

# Aggregate features per wallet
for tx in data:
    w = tx["userWallet"]
    action = tx["action"].lower()
    adata = tx["actionData"]
    usd_amt = 0.0
    try:
        amt = float(adata["amount"])
        price = float(adata.get("assetPriceUSD", 1.0))
        usd_amt = amt * price / (10**6 if "USD" in adata.get("assetSymbol","") else 10**18 if adata.get("assetSymbol","").startswith("W") else 1)
    except Exception:
        pass
    if action == "deposit":
        wallet_features[w]['deposit_count'] += 1
        wallet_features[w]['deposit_usd'] += usd_amt
    elif action == "borrow":
        wallet_features[w]['borrow_count'] += 1
        wallet_features[w]['borrow_usd'] += usd_amt
    elif action == "repay":
        wallet_features[w]['repay_count'] += 1
        wallet_features[w]['repay_usd'] += usd_amt
    elif action == "redeemunderlying":
        wallet_features[w]['redeem_count'] += 1
        wallet_features[w]['redeem_usd'] += usd_amt
    elif action == "liquidationcall":
        wallet_features[w]['liquidation_count'] += 1

# Features to DF
rows = []
for w, feats in wallet_features.items():
    rows.append({"wallet": w, **feats})
df = pd.DataFrame(rows)
df = df.fillna(0)

# Scoring logic (heuristic)
def score_row(row):
    score = 600
    score += min(row['deposit_usd']/1000, 200)            # scale up to +200 for high deposits
    score += min(row['repay_usd']/1000, 100)              # +100 for high repays
    score -= min(row['borrow_usd']/1000, 75)              # small penalty for large borrowing
    score -= 50 * row['liquidation_count']                # heavy penalty if liquidated
    score += 25 * min(row['repay_count'], row['borrow_count']) # reward for repays
    score = np.clip(score, 0, 1000)
    return int(score)
df['score'] = df.apply(score_row, axis=1)

df.sort_values("score", ascending=False).to_csv(OUTPUT_FILE, index=False)
print(f"[SUCCESS] Wallet scores saved to {OUTPUT_FILE}")

