import pandas as pd
import glob

# Step 1: Find all CSV files in the data folder
csv_files = glob.glob("data/*.csv")

all_data = []

for file in csv_files:
    df = pd.read_csv(file)

    # Remove extra spaces and standardize case
    df['product'] = df['product'].str.strip()
    df['product'] = df['product'].str.lower()

    # Keep only Pink Morsels
    df = df[df['product'] == 'pink morsel']

    # Clean price column: remove '$' and convert to float
    df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)

    # Calculate total sales
    df['sales'] = df['quantity'] * df['price']

    # Keep only required columns
    df = df[['sales', 'date', 'region']]
    all_data.append(df)

# Step 2: Combine and sort by date
final_df = pd.concat(all_data)
final_df = final_df.sort_values('date').reset_index(drop=True)

# Step 3: Save to formatted_sales.csv
final_df.to_csv('formatted_sales.csv', index=False)
print("formatted_sales.csv created successfully!")
print(f"Total rows: {len(final_df)}")
print(f"Date range: {final_df['date'].min()} to {final_df['date'].max()}")