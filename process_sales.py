import pandas as pd
import glob

# Step 1: Find all CSV files in the data folder
csv_files = glob.glob("data/*.csv")
all_data = []

for file in csv_files:
    df = pd.read_csv(file)

    # Remove extra spaces and standardize case
    df['product'] = df['product'].str.strip()   # remove leading/trailing spaces
    df['product'] = df['product'].str.lower()   # convert to lowercase

    # Keep only Pink Morsels
    df = df[df['product'] == 'pink morsel']

    # Clean price column: remove '$' and convert to float
    df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)

    # Calculate total sales
    df['sales'] = df['quantity'] * df['price']

    # Keep only required columns
    df = df[['sales', 'date', 'region']]
    all_data.append(df)

# Step 2: Combine all processed CSVs
final_df = pd.concat(all_data)

# Step 3: Save to formatted_sales.csv
final_df.to_csv('formatted_sales.csv', index=False)
print("formatted_sales.csv created successfully!")