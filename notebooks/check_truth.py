import pandas as pd
import numpy as np

# Read CSV files into DataFrames
df1 = pd.read_csv("extracted_deaths_info.csv")
df2 = pd.read_csv("who_data.csv")
country_mapping = {
    'United States': 'United States of America',
    'USA': 'US',
    'UK': 'GB',
    'America': 'United States of America',
    'United Kingdom' : 'United Kingdom of Great Britain and Northern Ireland',
    'Iran' : 'Iran (Islamic Republic of)'
}
df1['country'] = df1['country'].map(country_mapping).fillna(df1['country'])
# Convert date columns to datetime objects
df1['date'] = pd.to_datetime(df1['date'])
df2['Date_reported'] = pd.to_datetime(df2['Date_reported'])

# Define a function to find the closest date
def find_closest_date_row(date, df):
    closest_date_idx = df['Date_reported'].sub(date).abs().idxmin()
    return df.loc[[closest_date_idx]]

# List to store the results
results = []

for index, row in df1.iterrows():
    country = row['country']
    date = row['date']
    deaths = row['amount_of_deaths']
    
    # Find matching rows in the second DataFrame based on country
    matching_rows = df2[df2['Country'] == country]
    
    # If no matching rows based on country, try matching based on Country_code
    if matching_rows.empty:
        country_code = df2[df2['Country_code'] == country]
        if not country_code.empty:
            matching_rows = df2[df2['Country_code'] == country]
    
    if not matching_rows.empty:
        closest_date_row = find_closest_date_row(date, matching_rows)
        cumulative_deaths = closest_date_row['Cumulative_deaths'].values[0]
        
        # Calculate percentage error
        if deaths == 0:
            percentage_error = np.nan  # Set to NaN if deaths is zero
        else:
            percentage_error = abs(((cumulative_deaths - deaths) / deaths) * 100)
        
        # Determine if error is less than 10
        is_true = percentage_error < 10
        
        # Append results to the list
        results.append({
            'Country': country,
            'Date': date,
            'Amount_of_Deaths': deaths,
            'Cumulative_Deaths': cumulative_deaths,
            'Percentage_Error': percentage_error,
            'isTrue': is_true
        })
    else:
        print(f"No data found for country: {country}")

# Convert the list of dictionaries to a DataFrame
results_df = pd.DataFrame(results)

# Calculate mean error, ignoring NaN values
mean_error = results_df['Percentage_Error'].mean(skipna=True)

# Print mean error
print(f"Mean Error: {mean_error:.2f}%")

# Sort the DataFrame by Percentage_Error in ascending order
results_df.sort_values(by='Percentage_Error', ascending=True, inplace=True)

# Save the DataFrame to a CSV file
results_df.to_csv('percentage_errors.csv', index=False)
