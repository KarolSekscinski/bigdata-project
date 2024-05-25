import pandas as pd
from transformers import pipeline, TFAutoModelForSequenceClassification, AutoTokenizer
import time

# Read the CSV file
#df = pd.read_csv('tokenized_clean_tw.csv')
df = pd.read_csv('tokenized_clean_tw.csv')
#df = df[['original_text', 'created_at']]

# Select the first 50 rows (adjust for testing purposes, increase for full run)
df_first = df.sample(10000)

# Load the model and tokenizer
model_path = './saved_model'
model = TFAutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Initialize the classifier with the loaded model and tokenizer
start1 = time.time()
classifier = pipeline('zero-shot-classification', model=model, tokenizer=tokenizer, device=0, framework='tf')
end2 = time.time() - start1
print(f"TIME TO CREATE CLASSIFIER: {end2}s")

# Define candidate labels
candidate_labels = ['death', 'infection', 'vaccine']

# Counter for tracking rows and saving results
batch_size = 25
total_rows = len(df_first)
current_batch = 0

# Define a function to classify each tweet
def classify_tweet(tweet):
    try:
        result = classifier(tweet, candidate_labels)
        label_score_pairs = [(label, score) for label, score in zip(result['labels'], result['scores'])]
        label_score_pairs.insert(0, result['sequence'])
    except:
        label_score_pairs = [(label, score) for label, score in zip(candidate_labels, [0.0, 0.0, 0.0])]
    return label_score_pairs

# Create or clear the CSV file before starting the loop
output_file = 'classification_results.csv'
with open(output_file, 'w') as f:
    f.write('id,created_at,source,original_text,lang,favorite_count,retweet_count,original_author,hashtags,user_mentions,place,clean_tweet,compound,neg,neu,pos,sentiment\n')

# Apply the classification function to each tweet and save every 50 rows
start = time.time()
for start_index in range(0, total_rows, batch_size):
    end_index = min(start_index + batch_size, total_rows)
    df_chunk = df_first.iloc[start_index:end_index].copy()
    df_chunk['classification_results'] = df_chunk['clean_tweet'].apply(classify_tweet)
    
    # Append to CSV
    df_chunk.to_csv(output_file, mode='a', index=False, header=False)
    
    current_batch += 1
    print(f"Processed and saved batch {current_batch} of rows {start_index} to {end_index}")

end = time.time() - start
print(f"TOTAL TIME: {end}s")

# Display the last batch of classification results for verification
#print(df_chunk[['original_text', 'classification_results']])
