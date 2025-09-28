import pandas as pd

df = pd.read_json('transactions.json')
df = df[['purchase_date', 'amount', 'description']]  # select needed columns
df['purchase_date'] = pd.to_datetime(df['purchase_date'])
df = df.sort_values(by='purchase_date', ascending=False)
df['description'] = df['description'].fillna('').str.split().str[0]

category_totals = df.groupby('description', as_index=False)['amount'].sum()