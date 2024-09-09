import pandas as pd

# Step 1: Load the existing CSV file into a DataFrame
csv_path = '/Users/aravpant/Desktop/Projects/WebScraping/AddressList/small.csv'
df = pd.read_csv(csv_path)

# Step 2: Add a new column with some data (can be based on your logic)
# For example, adding a new column called 'New_Column' with default values
df['Google-1_Gig'] = '-'

# Step 3: Save the DataFrame back to the same CSV to make changes permanent
df.to_csv(csv_path, index=False)

print("Column added and file updated successfully.")
