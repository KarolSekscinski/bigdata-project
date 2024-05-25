import pandas as pd
from transformers import AutoTokenizer
import time

model_path = './saved_model'
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Read the CSV file
df = pd.read_csv('clean_tw-1.csv')


# Define a function to tokenize text
def tokenize_text(text):
    try:
        tokens = tokenizer.tokenize(text)
        tokenized_text = ' '.join(tokens)
    except:
        return ''
    return tokenized_text

start1 = time.time()
df['clean_tweet'] = df['original_text'].apply(tokenize_text)
end2 = time.time() - start1
print(f"TIME TO CREATE CLASSIFIER: {end2}s")

output_file = 'tokenized_clean_tw.csv'
df.to_csv(output_file, index=False)

print(f"Tokenized text saved to {output_file}")
