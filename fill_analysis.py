import pandas as pd
import matplotlib.pyplot as plt

bins = [0, 100, 200, 500, 800, 1000]
labels = ["0–100", "100–200", "200–500", "500–800", "800–1000"]
df = pd.read_csv('wallet_scores.csv')
df['score_range'] = pd.cut(df['score'], bins, labels=labels, include_lowest=True)
dist = df['score_range'].value_counts().sort_index()

print('Wallet Score Distribution:')
print(dist)

# Bar plot for score ranges
dist.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Wallet Credit Score Distribution')
plt.xlabel('Score Range')
plt.ylabel('Wallet Count')
plt.tight_layout()
plt.savefig('wallet_score_distribution.png')
plt.close()

# Histogram of all scores
df['score'].plot(kind='hist', bins=[0,100,200,500,800,1000], color='limegreen', edgecolor='black', rwidth=0.85)
plt.title('Wallet Score Histogram')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('wallet_score_histogram.png')
plt.close()

# Update analysis.md with real values, and embed plots (markdown)
template = '''# Wallet Score Analysis\n\nThis document provides an analysis of wallet scores generated from Aave v2 transaction data.\n\n## Score Distribution\n\n![Bar Plot of Wallet Credit Score Ranges](wallet_score_distribution.png)\n\n![Histogram of All Wallet Scores](wallet_score_histogram.png)\n\n- **0–100**: Very high-risk, often liquidated, or only borrowing with little repayment\n- **100–200**: High-risk users, many borrow actions, few repays\n- **200–500**: Some responsible action, occasional risky activity\n- **500–800**: Most wallets, fairly balanced, regular deposits and repayments\n- **800–1000**: Highly reliable, high deposits, regular repayments, no liquidation calls\n\n| Score Range | Wallet Count | Notable Patterns                       |\n|-------------|-------------|----------------------------------------|\n| 0–100       | {a}          | Heavy liquidations, aggressive borrow  |\n| 100–200     | {b}          | Many borrows, few repayments           |\n| 200–500     | {c}          | Mixed repays/deposits, some risk       |\n| 500–800     | {d}          | Deposits, repays frequent, steady      |\n| 800–1000    | {e}          | No liquidations, frequent repayments   |\n\n### Behavioral Patterns\n- **Low scores** are associated with wallets that borrowed large sums, rarely repaid, and/or triggered liquidation.\n- **Medium scores** indicate activity diversity with some repayments and borrows, occasional risky behavior.\n- **High scores** show consistent deposits, repayments, and lack of risky actions.\n\n---\n\n**Project by KassITsolutions, 2025**\n'''.format(a=dist.get('0–100',0), b=dist.get('100–200',0), c=dist.get('200–500',0), d=dist.get('500–800',0), e=dist.get('800–1000',0))

with open('analysis.md', 'w') as f:
    f.write(template)

print('[SUCCESS] analysis.md updated with actual wallet score distribution and plots.')

