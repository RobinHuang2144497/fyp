import pandas as pd

# Read multiple Excel files
file1 = r'D:\\桌面\\TRD_FwardQuotation.xlsx'
file2 = r'D:\\桌面\\TRD_FwardQuotation1.xlsx'
file3 = r'D:\\桌面\\TRD_FwardQuotation2.xlsx'
file4 = r'D:\\桌面\\TRD_FwardQuotation3.xlsx'
file5 = r'D:\\桌面\\TRD_FwardQuotation4.xlsx'

# Read each Excel file into a DataFrame
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)
df3 = pd.read_excel(file3)
df4 = pd.read_excel(file4)
df5 = pd.read_excel(file5)

# Concatenate all DataFrames into one
merged_df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

# Output the merged DataFrame as a JSON file
json_output = merged_df.to_json(r'D:\\桌面\\merged_data.json', orient='records', lines=True)

print("Data merged and successfully saved as a JSON file!")
