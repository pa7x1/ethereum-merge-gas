import pandas as pd
from pathlib import Path
import plotly.express as px

pow_data_fp = Path('../static/pow.json')
pos_data_fp = Path('../static/pos.json')
GWEI = 1_000_000_000


pow_df = pd.read_json(pow_data_fp)
pow_df['baseFeePerGas'] = pow_df['baseFeePerGas'].apply(int, base=16) / GWEI
pow_df['gasLimit'] = pow_df['gasLimit'].apply(int, base=16)
pow_df['gasUsed'] = pow_df['gasUsed'].apply(int, base=16)
pow_df['number'] = pow_df['number'].apply(int, base=16)
pow_df['size'] = pow_df['size'].apply(int, base=16)
pow_df['timestamp'] = pow_df['timestamp'].apply(int, base=16)
pow_df['timestampDiff'] = pow_df['timestamp'].diff()

pos_df = pd.read_json(pos_data_fp)
pos_df['baseFeePerGas'] = pos_df['baseFeePerGas'].apply(int, base=16) / GWEI
pos_df['gasLimit'] = pos_df['gasLimit'].apply(int, base=16)
pos_df['gasUsed'] = pos_df['gasUsed'].apply(int, base=16)
pos_df['number'] = pos_df['number'].apply(int, base=16)
pos_df['size'] = pos_df['size'].apply(int, base=16)
pos_df['timestamp'] = pos_df['timestamp'].apply(int, base=16)
pos_df['timestampDiff'] = pos_df['timestamp'].diff()

df = pd.DataFrame()
df['PoW Base Fee'] = pow_df['baseFeePerGas']
df['PoS Base Fee'] = pos_df['baseFeePerGas']
stats = df.describe()

print(stats.to_markdown())


fig = px.histogram(df, x=['PoS Base Fee', 'PoW Base Fee'], cumulative=True, histnorm="percent",
                   title="Ethereum Gas Fee eCDF - Proof of Work vs Proof of Stake")
fig.update_xaxes(title_text='Base Fee (GWei)', dtick=5)
fig.update_yaxes(title_text="percent (%)")
fig.update_layout(barmode="overlay")
fig.show()
