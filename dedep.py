import pandas as pd
import os

# Function to deduplicate based on URL column
def deduplicate_csv(input_csv, output_csv):
    # Check if the input CSV exists
    if not os.path.exists(input_csv):
        print(f"Input CSV file '{input_csv}' not found.")
        return
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_csv)
    
    # Check if the 'URL' column exists in the CSV
    if 'URL' not in df.columns:
        print("The 'URL' column was not found in the CSV.")
        return
    
    # Drop duplicate rows based on the 'URL' column, keeping the first occurrence
    df_deduplicated = df.drop_duplicates(subset='URL', keep='first')
    
    # Write the deduplicated DataFrame to a new CSV file
    df_deduplicated.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Deduplicated CSV saved to '{output_csv}'.")

# Main function to handle input and output CSV files
def main():
    input_csv = 'scraped_news/cava_articles.csv'  # Input CSV file path
    output_csv = 'scraped_news/cava_articles_deduplicated.csv'  # Output CSV file path for deduplicated data

    # Call the deduplication function
    deduplicate_csv(input_csv, output_csv)

if __name__ == "__main__":
    main()
