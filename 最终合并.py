import pandas as pd

# File paths
file1 = r'D:\\桌面\\1.xlsx'
file2 = r'D:\\桌面\\2.xlsx'

# Read the two Excel files into DataFrames
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# Ensure that 'TradingDate' is in datetime format in both DataFrames
df1['TradingDate'] = pd.to_datetime(df1['TradingDate'], errors='coerce')
df2['TradingDate'] = pd.to_datetime(df2['TradingDate'], errors='coerce')

# Ensure that 'Symbol' is treated as a string in both DataFrames
df1['Symbol'] = df1['Symbol'].astype(str)
df2['Symbol'] = df2['Symbol'].astype(str)

# Merge the two DataFrames on 'Symbol' and 'TradingDate', keeping rows from df1 and filling unmatched rows with NaN (null)
merged_df = pd.merge(df1, df2, how='left', left_on=['Symbol', 'TradingDate'], right_on=['Symbol', 'TradingDate'])

# Output the merged DataFrame as a JSON file on the desktop
json_output = merged_df.to_json(r'D:\\桌面\\merged_data.json', orient='records', lines=True)

print("Data merged and successfully saved as JSON file!")
