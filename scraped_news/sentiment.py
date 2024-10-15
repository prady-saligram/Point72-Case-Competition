import pandas as pd
import os
import torch
import torch.nn.functional as F
from transformers import BertTokenizer, BertForSequenceClassification

# Optional: Disable symlink warning for Hugging Face cache on Windows
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

# Load pre-trained FinBERT model from Hugging Face
model_name = "ProsusAI/finbert"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Function to calculate softmax to get probabilities
def softmax(logits):
    return F.softmax(torch.tensor(logits), dim=-1).tolist()

# Function to get sentiment classification and confidence scores
def get_sentiment_with_confidence(text):
    try:
        # Tokenize input text
        inputs = tokenizer(text[:512], return_tensors="pt", truncation=True)

        # Pass inputs to the model
        outputs = model(**inputs)

        # Get the logits (raw scores for each class)
        logits = outputs.logits.detach().numpy()[0]

        # Apply softmax to get probabilities for each label
        probs = softmax(logits)

        # Define the mapping for the labels
        sentiment_map = {
            0: 'Negative',  # Corresponds to LABEL_0
            1: 'Neutral',   # Corresponds to LABEL_1
            2: 'Positive'   # Corresponds to LABEL_2
        }

        # Get the label with the highest probability
        predicted_label = logits.argmax()

        # Return the predicted sentiment and the confidence scores
        sentiment_value = sentiment_map[predicted_label]
        return sentiment_value, probs
    except Exception as e:
        return None, [0.0, 0.0, 0.0]  # Handle errors, return None and zero confidence

# Load your CSV file (cava_articles.csv)
input_csv_path = "cava_articles_reindexed.csv"  # Replace with the actual path to your CSV file
df = pd.read_csv(input_csv_path)

# Apply sentiment analysis to the 'Content' column
df['Sentiment'], df['Confidence_Scores'] = zip(*df['Content'].apply(lambda content: get_sentiment_with_confidence(str(content))))

# Split the confidence scores into individual columns
df[['Negative_Confidence', 'Neutral_Confidence', 'Positive_Confidence']] = pd.DataFrame(df['Confidence_Scores'].tolist(), index=df.index)

# Drop the intermediate confidence score list
df.drop(columns=['Confidence_Scores'], inplace=True)

# Save the updated dataframe with sentiment and confidence to a new CSV
output_csv_path = "final_cava_sentiment.csv"
df.to_csv(output_csv_path, index=False)

print(f"Sentiment analysis complete. Results saved to {output_csv_path}.")
