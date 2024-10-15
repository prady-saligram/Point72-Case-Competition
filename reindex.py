import pandas as pd
import os

# Function to reindex the 'ID' column to consecutive integers
def reindex_csv(input_csv, output_csv):
    # Check if the input CSV exists
    if not os.path.exists(input_csv):
        print(f"Input CSV file '{input_csv}' not found.")
        return
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_csv)
    
    # Check if the 'ID' column exists in the CSV
    if 'ID' not in df.columns:
        print("The 'ID' column was not found in the CSV.")
        return
    
    # Reindex the 'ID' column to be consecutive integers starting from 1
    df['ID'] = range(1, len(df) + 1)
    
    # Write the updated DataFrame to a new CSV file
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Reindexed CSV saved to '{output_csv}'.")

# Main function to handle input and output CSV files
def main():
    input_csv = 'scraped_news/cava_articles_updated.csv'  # Input CSV file path
    output_csv = 'scraped_news/cava_articles_reindexed.csv'  # Output CSV file path for reindexed data

    # Call the reindexing function
    reindex_csv(input_csv, output_csv)

if __name__ == "__main__":
    main()
