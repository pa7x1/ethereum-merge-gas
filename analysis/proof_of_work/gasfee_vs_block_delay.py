import pandas as pd
from pathlib import Path
import plotly.express as px

block_data_fp = Path('../../static/pow.json')
GWEI = 1_000_000_000


df = pd.read_json(block_data_fp)
df['baseFeePerGas'] = df['baseFeePerGas'].apply(int, base=16) / GWEI
df['gasLimit'] = df['gasLimit'].apply(int, base=16)
df['gasUsed'] = df['gasUsed'].apply(int, base=16)
df['number'] = df['number'].apply(int, base=16)
df['size'] = df['size'].apply(int, base=16)
df['timestamp'] = df['timestamp'].apply(int, base=16)
df['timestampDiff'] = df['timestamp'].diff()

df['baseFeePerGasEMA30'] = df['baseFeePerGas'].ewm(span=30).mean()
df['baseFeePerGasGrowth'] = df['baseFeePerGas'] - df['baseFeePerGasEMA30']


df['averageBlocktime'] = df['timestampDiff'].rolling(window=30).mean()
df['averageBlocktimeEMA30'] = df['averageBlocktime'].ewm(span=30).mean()
df['blockTimeGrowth'] = df['averageBlocktime'] - df['averageBlocktimeEMA30']

fig = px.scatter(x=df['blockTimeGrowth'], y=df['baseFeePerGasGrowth'], marginal_x="violin", marginal_y="violin",
                 title="Ethereum Proof of Work - Base Fee vs Block Delay")
fig.update_xaxes(title_text='Change in Average Block Time (\u0394s/block)')
fig.update_yaxes(title_text="Change in Base Fee (GWei)")
fig.show()


print(df[['blockTimeGrowth', 'baseFeePerGasGrowth']].corr(method="spearman").to_markdown())
