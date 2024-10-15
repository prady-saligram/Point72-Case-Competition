# 📊 **Point 72 Case Competition: AI Sentiment Analysis**

Welcome to the **Point 72 Case Competition** project! In this pipeline, we analyze the most recent news articles on **CAVA** using AI-driven sentiment analysis. This project automates the process of scraping articles, conducting sentiment analysis, and visualizing sentiment trends. Below is a detailed description of the pipeline.

---

## 🚀 **Pipeline Overview**

### 1. **Article Scraping**
The first stage of the pipeline involves scraping the latest news articles related to **CAVA**. This is achieved using an automated web scraper that extracts essential metadata such as article titles, publication time, URLs, and the content of the articles. The scraper is designed to collect a wide array of news articles from various sources, ensuring a comprehensive dataset for analysis. Once the scraping process is complete, the articles are saved in a CSV file, which serves as the input for sentiment analysis.

### 2. **Sentiment Analysis**
In the second stage, the scraped articles are subjected to a sentiment analysis model. This model assesses the **positive**, **negative**, and **neutral** tones of the articles based on their content. For each article, sentiment scores are calculated, and confidence levels are assigned to reflect the likelihood of each sentiment class. The sentiment analysis provides valuable insights into how the media perceives CAVA, as the results indicate whether recent articles skew towards positive or negative sentiment. These results are appended to the CSV dataset.

### 3. **Visualization of Sentiment Trends**
In the final stage, the sentiment scores from the analyzed articles are used to generate visual representations of the sentiment trends over time. These visualizations include:

- **Positive Sentiment Over Time**: A graph showcasing the fluctuation of positive sentiment in news articles over time.
- **Negative Sentiment Over Time**: A similar graph displaying negative sentiment.
- **Comparison of Sentiments**: A combined graph that compares both positive and negative sentiments over time, revealing any correlation between the two.
- **Confidence Interval Visualization**: Shaded regions in the graphs indicate confidence intervals, highlighting the periods with high confidence in the sentiment classification.

These visualizations help identify patterns in the news sentiment regarding CAVA, such as periods of overhype, fluctuations in negative sentiment, or overall media perception over time. This step is crucial in understanding how public sentiment shifts in response to significant events or trends related to CAVA.
