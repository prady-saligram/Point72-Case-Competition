# 📊 **Point 72 Case Competition: AI Sentiment Analysis**

Welcome to AllStreet's AI sentiment analysis scope of our CAVA short! In this pipeline, we analyze the most recent news articles on **CAVA** using AI-driven sentiment analysis, where we automate the process of scraping articles, conducting sentiment analysis, and visualizing sentiment trends.

---

## 🚀 **Pipeline Overview**

### 1. **Article Scraping**
The first stage of the pipeline involves scraping the latest news articles related to **CAVA**, which is done using an automated web scraper that extracts essential metadata such as article titles, publication time, URLs, and the content of the articles. The scraper is designed to collect a wide array of news articles from various sources, ensuring a comprehensive dataset for analysis.

### 2. **Sentiment Analysis**
In the second stage, the scraped articles are subjected to a sentiment analysis model, where the FinBERT transformer language model assesses the **positive**, **negative**, and **neutral** tones of the articles based on their content. For each article, sentiment scores are calculated, and confidence levels are assigned to reflect the likelihood of each sentiment class by simply adding a softmax layer to the output probabilities. 

### 3. **Visualization of Sentiment Trends**
In the final stage, the sentiment scores from the analyzed articles are used to generate visual representations of the sentiment trends over time. These visualizations include:

- **Positive Sentiment Over Time**: A graph showcasing the fluctuation of positive sentiment in news articles over time.
- **Negative Sentiment Over Time**: A similar graph displaying negative sentiment.
- **Confidence Interval Visualization**: Shaded regions in the graphs indicate confidence intervals, highlighting the periods with high confidence in the sentiment classification.

These visualizations help identify patterns in the news sentiment regarding CAVA, such as periods of overhype, fluctuations in negative sentiment, or overall media perception over time—all of which are crucial in understanding how pundit sentiment can signal overvaluation perceptions of entities (CAVA, in this case).
