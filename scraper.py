import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Step 1: Initialize the CSV File
def initialize_csv(output_file):
    headers = ["ID", "Scrape_Time", "Publication_Time", "URL", "Source", "Title", "Content", "Sentiment"]
    if not os.path.exists(output_file):
        df = pd.DataFrame(columns=headers)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Initialized CSV file: {output_file}")

# Step 2: Create WebDriver instance
def create_driver():
    chrome_driver_path = "C:/Users/prady/chromedriver-win64/chromedriver.exe"  # Update this path to your ChromeDriver path
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Hide the webdriver property to avoid detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

# Step 3: Scroll and scrape articles
def scroll_and_scrape(driver, output_file):
    base_url = "https://finance.yahoo.com/quote/CAVA/news/"
    driver.get(base_url)

    article_counter = 1
    scraped_articles = []

    # Infinite scroll logic
    while True:
        time.sleep(3)  # Allow time for page content to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Scrape the articles from the current scroll
        articles = soup.find_all('li', class_='stream-item story-item yf-1usaaz9')
        for article in articles:
            try:
                # Extract title and URL
                title_tag = article.find('a', class_='subtle-link')
                title = title_tag.get('title', 'No Title').strip()
                full_url = title_tag.get('href', 'No URL').strip()

                # Extract content
                content_tag = article.find('p', class_='clamp')
                content = content_tag.text.strip() if content_tag else 'No Content'

                # Publication time and source
                footer = article.find('div', class_='footer')
                publication_info = footer.find('div', class_='publishing').text if footer else 'No Publication Info'
                publication_time = ' '.join(publication_info.split()[-2:])

                scrape_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Save each article data in the CSV
                scraped_articles.append({
                    'ID': article_counter,
                    'Scrape_Time': scrape_time,
                    'Publication_Time': publication_time,
                    'URL': full_url,
                    'Source': 'Yahoo Finance',
                    'Title': title,
                    'Content': content,
                    'Sentiment': ''  # Leave blank for future sentiment analysis
                })

                article_counter += 1
            except Exception as e:
                print(f"Error extracting article: {e}")

        # Save articles in batches
        if scraped_articles:
            df = pd.DataFrame(scraped_articles)
            df.to_csv(output_file, mode='a', header=False, index=False, encoding='utf-8')
            scraped_articles = []

        # Scroll down and check if more articles load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new articles to load
        
        # Check if there's a "load more" button or end of content
        try:
            end_of_content = driver.find_element(By.CSS_SELECTOR, 'div.stream-end')
            if end_of_content:
                print("End of content reached")
                break
        except NoSuchElementException:
            continue  # Continue scrolling if end not reached

# Step 4: Main function
def main():
    output_dir = 'scraped_news'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'cava_articles.csv')

    # Initialize the CSV with the required columns
    initialize_csv(output_file)

    # Create a WebDriver instance
    driver = create_driver()

    try:
        # Start scraping and scrolling
        scroll_and_scrape(driver, output_file)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
