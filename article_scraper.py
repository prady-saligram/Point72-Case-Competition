import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Step 1: Initialize CSV with the required format
def initialize_csv(links_output_file):
    headers = ["ID", "Scrape_Time", "Publication_Time", "URL", "Source", "Title", "Content", "Sentiment"]
    if not os.path.exists(links_output_file):
        df = pd.DataFrame(columns=headers)
        df.to_csv(links_output_file, index=False, encoding='utf-8')
        print(f"Initialized CSV file: {links_output_file}")

# Step 2: Format the publication date to ensure only seconds are present
def format_publication_time(datetime_str):
    try:
        # The original format is '2024-10-13T07:47:00.000Z'
        # We will remove the milliseconds by splitting and only keeping the first part
        formatted_time = datetime_str.split('.')[0].replace('T', ' ')
        return formatted_time
    except Exception as e:
        print(f"Error formatting datetime: {e}")
        return "NA"

# Step 3: Scrape each article's details and handle "Sign in" messages
def get_article_details(driver, url, article_id):
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(2)
    
    # Scrape publication time
    try:
        pub_time_elem = driver.find_element(By.CSS_SELECTOR, 'time.byline-attr-meta-time')
        pub_time = pub_time_elem.get_attribute('datetime')
        formatted_pub_time = format_publication_time(pub_time)
    except NoSuchElementException:
        formatted_pub_time = 'NA'
        print(f"[DEBUG] Could not find publication time for article {article_id}")

    # Scrape content
    try:
        content_elem = driver.find_element(By.CSS_SELECTOR, 'div.body.yf-5ef8bf')
        paragraphs = content_elem.find_elements(By.TAG_NAME, 'p')
        content = " ".join([p.text.strip() for p in paragraphs])

    except NoSuchElementException:
        print(f"[DEBUG] Could not find content for article {article_id}")

    return formatted_pub_time, content

# Step 4: Write article data to CSV
def write_row_to_csv(row_data, output_file):
    df = pd.DataFrame([row_data])
    df.to_csv(output_file, mode='a', header=False, index=False, encoding='utf-8')
    print(f"Dynamically wrote article {row_data['ID']} to CSV.")

# Step 5: Scrape and update the new CSV dynamically without multithreading
def update_new_csv_with_scraped_info(old_csv_file, new_csv_file):
    # Load the old CSV file
    df_old = pd.read_csv(old_csv_file)

    # Initialize the new CSV
    initialize_csv(new_csv_file)

    # Create WebDriver instance
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Scrape each article sequentially and update the CSV
    for index, row in df_old.iterrows():
        try:
            article_id = row['ID']
            url = row['URL']
            pub_time, content = get_article_details(driver, url, article_id)

            # Prepare the new row with updated publication time and content
            row_data = {
                'ID': article_id,
                'Scrape_Time': row['Scrape_Time'],
                'Publication_Time': pub_time,  # Newly scraped publication time
                'URL': row['URL'],
                'Source': row['Source'],
                'Title': row['Title'],
                'Content': content,  # Newly scraped content
                'Sentiment': 'NA'  # Leave sentiment as "NA" for now
            }

            # Write this row dynamically to the new CSV
            write_row_to_csv(row_data, new_csv_file)

        except Exception as e:
            print(f"Error processing article {row['ID']}: {e}")

    # Close the driver after all processing
    driver.quit()

# Main function
def main():
    old_csv_file = 'scraped_news/cava_articles.csv'  # Path to the old CSV
    new_csv_file = 'scraped_news/cava_articles_updated.csv'  # Path to the new CSV

    if not os.path.exists(old_csv_file):
        print(f"CSV file {old_csv_file} not found.")
        return

    # Scrape data and update the new CSV
    update_new_csv_with_scraped_info(old_csv_file, new_csv_file)

if __name__ == "__main__":
    main()
