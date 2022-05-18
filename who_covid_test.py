import pandas as pd

url = 'data/ethiopia.csv'
df = pd.read_csv(url, keep_default_na=False)
df['Date_reported'] = pd.to_datetime(df['Date_reported'])

df_series = df.copy(deep=True)
df_series['Average_cases_7_days_per_100000'] = df_series['New_cases'].rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)
df_series['Average_cases_7_days_per_100000_pc_change'] = df_series['Average_cases_7_days_per_100000'].pct_change() * 100
print(df_series)

df = df.resample('W', on='Date_reported').sum().reset_index()
df['weekly_new_cases_pc_change'] = df['New_cases'].pct_change() * 100
print(df)
