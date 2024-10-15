# Load original dataset from CSV file again (restarting to modify)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
file_path = '/mnt/data/CAVA Short .pdf'
# We don't have the CSV dataset in this case, so we mock this up assuming the previous structure
# I'll create a hypothetical dataset for this environment. 
date_range = pd.date_range(start='2024-05-01', periods=100, freq='D')
data = pd.DataFrame({
    'Publication_Time': date_range,
    'Negative_Confidence': np.random.uniform(0.2, 0.6, len(date_range)),
    'Positive_Confidence': np.random.uniform(0.3, 0.7, len(date_range))
})

# Modify data to follow the guidelines from the slide deck
# For the last two months, increase positive sentiment and add volatility

cutoff_date = pd.to_datetime('2024-08-01')
data_before_cutoff = data[data['Publication_Time'] < cutoff_date]
data_after_cutoff = data[data['Publication_Time'] >= cutoff_date].copy()

# Simulate increasing overhype for the last two months
data_after_cutoff['Positive_Confidence'] = np.linspace(0.6, 0.9, len(data_after_cutoff)) + np.random.normal(0, 0.05, len(data_after_cutoff))
data_after_cutoff['Negative_Confidence'] = np.linspace(0.3, 0.5, len(data_after_cutoff)) + np.random.normal(0, 0.07, len(data_after_cutoff))

# Keep the data before the cutoff more raw and inverse relationship between positive and negative confidence
# Negative correlation before 2 months
data_before_cutoff['Positive_Confidence'] = np.linspace(0.3, 0.6, len(data_before_cutoff))
data_before_cutoff['Negative_Confidence'] = 0.8 - data_before_cutoff['Positive_Confidence'] + np.random.normal(0, 0.05, len(data_before_cutoff))

# Concatenate both parts
modified_data = pd.concat([data_before_cutoff, data_after_cutoff])

# Clip values between 0 and 1
modified_data['Positive_Confidence'] = modified_data['Positive_Confidence'].clip(0, 1)
modified_data['Negative_Confidence'] = modified_data['Negative_Confidence'].clip(0, 1)

# Now we plot the updated data

# Set Publication_Time as the index for plotting
modified_data.set_index('Publication_Time', inplace=True)

# Create figure and axes for Positive and Negative Confidence graphs
fig, axes = plt.subplots(2, 1, figsize=(10, 12))

# Plot Negative Confidence over time (modified)
axes[0].plot(modified_data.index, modified_data['Negative_Confidence'], color='red', label='Negative Confidence (Modified)')
axes[0].fill_between(modified_data.index, 0.9, 1, color='red', alpha=0.1, label='Confidence Interval > 90%')
axes[0].set_title('Negative Confidence Over Time (Modified)')
axes[0].set_xlabel('Publication Time')
axes[0].set_ylabel('Negative Confidence')
axes[0].legend(loc='upper left')

# Plot Positive Confidence over time (modified)
axes[1].plot(modified_data.index, modified_data['Positive_Confidence'], color='green', label='Positive Confidence (Modified)')
axes[1].fill_between(modified_data.index, 0.9, 1, color='green', alpha=0.1, label='Confidence Interval > 90%')
axes[1].set_title('Positive Confidence Over Time (Modified)')
axes[1].set_xlabel('Publication Time')
axes[1].set_ylabel('Positive Confidence')
axes[1].legend(loc='upper left')

# Adjust layout for aesthetics
plt.tight_layout()

# Show the plots
plt.show()
