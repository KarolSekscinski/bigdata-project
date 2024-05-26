import pandas as pd
import ast

df = pd.read_csv('classification_results.csv')

def extract_death_score(sentiment):
    try:
        sentiment_list = ast.literal_eval(sentiment)
        for item in sentiment_list:
            if 'death' in item:
                return item[1]  
    except (ValueError, SyntaxError):
        return 0.0

df['death_score'] = df['sentiment'].apply(extract_death_score)

df['death_score'] = pd.to_numeric(df['death_score'], errors='coerce')

df = df.dropna(subset=['death_score'])

df_sorted = df.sort_values(by='death_score', ascending=False)

output_file = 'sorted_by_death_score.csv'

df_sorted.to_csv(output_file, index=True)