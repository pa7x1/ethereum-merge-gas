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

df_stats = df.describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95])
print(df_stats['baseFeePerGas'])

fig = px.histogram(x=df['baseFeePerGas'], histnorm='percent', title="Ethereum Proof of Work - Base Fee Histogram")
fig.update_xaxes(title_text='Base Fee (GWei)', dtick=5)
fig.update_yaxes(title_text="percent (%)", dtick=0.5)
fig.show()

print()