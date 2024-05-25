import pandas as pd
from transformers import pipeline, TFAutoModelForSequenceClassification, AutoTokenizer
import time
# Read the CSV file
df = pd.read_csv('clean_tw-1.csv')
df = df[['original_text','created_at']]
# Select the first 50 rows
df_first = df.head(5)

#Load the model and tokenizer
model_path = './saved_model'
model = TFAutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Initialize the classifier with the loaded model and tokenizer
start1 = time.time()
classifier = pipeline('zero-shot-classification', model=model, tokenizer=tokenizer)
end2 = time.time() - start1
time_spent2 = end2
print(f"TIME TO CREATE CLASSIFIER:{time_spent2}s!!!!!!!!!!!!!!!!!!!!!!!!!!")
# Define candidate labels
candidate_labels = ['death', 'infection', 'vaccine'] # VACCINE

huj = 0
# Define a function to classify each tweet
def classify_tweet(tweet):
    global huj
    result = classifier(tweet, candidate_labels)
    label_score_pairs = [(label, score) for label, score in zip(result['labels'], result['scores'])]
    if huj == 50:
        print(huj)
        huj = 0
    huj += 1
    return label_score_pairs



# Apply the classification function to each tweet
start = time.time()
df_first['classification_results'] = df_first['original_text'].apply(classify_tweet)
end = time.time() - start
time_spent = end
print(f"TIME:{time_spent}s!!!!!!!!!!!!!!!!!!!!!!!!!!")

# Display the classification results
print(df_first[['original_text', 'classification_results']])
