# Wallet Credit Scoring using Aave V2 Transaction Data

## Overview
This project assigns a credit score (0–1000) to DeFi wallets based on their historical Aave V2 transaction behavior. The score is purely data-driven, with higher scores reflecting reliability and responsible interaction, and lower scores reflecting risky or exploitative behavior.

## Data & Features
- **Input:** `user-wallet-transactions.json` (raw transaction-level data)
- **Actions Processed:** `deposit`, `borrow`, `repay`, `redeemunderlying`, `liquidationcall`
- **Features Extracted per Wallet:**
  - Total and count of deposits, borrows, repays, and redeems (in USD, normalized where possible)
  - Count of liquidation events
  - Diversity and balance of actions

## Scoring Logic
For each wallet:
- Begin at a base score of **600**
- **High deposit and repay volumes** improve the score (normalized, capped bonus)
- **High borrow volume** slightly reduces the score
- **Liquidations** subtract heavily (penalty per event)
- **More repays than borrows** yields a bonus (responsible management)
- The score is clipped in the 0–1000 range

> See `score_wallets.py` for full scoring and normalization details.

## Usage
1. Ensure you have Python, pandas, numpy installed
2. Run:
   ```bash
   python score_wallets.py
   ```
   This will generate `wallet_scores.csv` with wallet addresses and scores.

## Outputs
- `wallet_scores.csv`: Wallet address, features, and score per wallet
- `analysis.md`: Distribution analysis of scores, behavioral insights

## Extending
- Scoring logic is in one place (`score_wallets.py`) for transparency
- Add features (e.g., time-weighted actions, protocol diversity, etc.) for more granularity
- Package and modularize for scaling or new protocols

---
For technical details and analysis, see `score_wallets.py` and `analysis.md`.
   - Ensure IP whitelist includes your IP (if configured)

2. **Order Placement Failures**
   - Check account balance
   - Verify symbol is correct and tradeable
   - Ensure quantity meets minimum requirements

3. **Connection Issues**
   - Check internet connectivity
   - Verify Binance API is accessible
   - Try using testnet for testing

### Getting Help

1. Check the `bot.log` file for detailed error messages
2. Verify your API credentials and permissions
3. Test with small amounts on testnet first
4. Ensure all dependencies are installed correctly

## Disclaimer

This bot is for educational and research purposes. Always:
- Test thoroughly on testnet before live trading
- Start with small amounts
- Monitor your positions actively
- Understand the risks involved in futures trading
- Use proper risk management

Trading cryptocurrency futures involves substantial risk and may not be suitable for all investors.
