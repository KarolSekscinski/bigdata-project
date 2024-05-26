import pandas as pd
import re

# Read the CSV file
df = pd.read_csv('sorted_by_death_score.csv',index_col=False)
df = df.head(1000)
df_who = pd.read_csv('who_data.csv',index_col=False)
countries = countries = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "American Samoa",
    "Andorra",
    "Angola",
    "Anguilla",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Aruba",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bermuda",
    "Bhutan",
    "Bolivia (Plurinational State of)", "Bolivia",
    "Bonaire, Saint Eustatius and Saba", "BES Islands",
    "Bosnia and Herzegovina", "Bosnia",
    "Botswana",
    "Brazil",
    "British Virgin Islands", "BVI",
    "Brunei Darussalam", "Brunei",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cabo Verde", "Cape Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Cayman Islands",
    "Central African Republic", "CAR",
    "Chad",
    "Chile",
    "China", "PRC (People's Republic of China)",
    "Colombia",
    "Comoros",
    "Congo", "Republic of the Congo", "Congo-Brazzaville",
    "Cook Islands",
    "Costa Rica",
    "Côte d'Ivoire", "Ivory Coast",
    "Croatia",
    "Cuba",
    "Curaçao",
    "Cyprus",
    "Czechia", "Czech Republic",
    "Democratic People's Republic of Korea", "North Korea",
    "Democratic Republic of the Congo", "DR Congo", "Congo-Kinshasa",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini", "Swaziland",
    "Ethiopia",
    "Falkland Islands (Malvinas)", "Falkland Islands",
    "Faroe Islands",
    "Fiji",
    "Finland",
    "France",
    "French Guiana",
    "French Polynesia",
    "Gabon",
    "Gambia", "The Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Gibraltar",
    "Greece",
    "Greenland",
    "Grenada",
    "Guadeloupe",
    "Guam",
    "Guatemala",
    "Guernsey",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Holy See", "Vatican City",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran (Islamic Republic of)", "Iran",
    "Iraq",
    "Ireland", "Republic of Ireland",
    "Isle of Man",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jersey",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Kosovo (in accordance with UN Security Council resolution 1244 (1999))", "Kosovo",
    "Kuwait",
    "Kyrgyzstan",
    "Lao People's Democratic Republic", "Laos",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Martinique",
    "Mauritania",
    "Mauritius",
    "Mayotte",
    "Mexico",
    "Micronesia (Federated States of)", "Micronesia",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Montserrat",
    "Morocco",
    "Mozambique",
    "Myanmar", "Burma",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands (Kingdom of the)", "Netherlands",
    "New Caledonia",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "Niue",
    "North Macedonia", "Macedonia",
    "Northern Mariana Islands",
    "Norway",
    "occupied Palestinian territory, including east Jerusalem", "Palestine",
    "Oman",
    "Pakistan",
    "Palau",
    "Panama",
    "Papua New Guinea", "PNG",
    "Paraguay",
    "Peru",
    "Philippines",
    "Pitcairn",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "Republic of Korea", "South Korea",
    "Republic of Moldova", "Moldova",
    "Réunion",
    "Romania",
    "Russian Federation", "Russia",
    "Rwanda",
    "Saint Barthélemy", "St. Barts",
    "Saint Helena",
    "Saint Kitts and Nevis", "St. Kitts and Nevis",
    "Saint Lucia", "St. Lucia",
    "Saint Martin (French part)",
    "Saint Pierre and Miquelon",
    "Saint Vincent and the Grenadines", "St. Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Sint Maarten (Dutch part)",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Syrian Arab Republic", "Syria",
    "Tajikistan",
    "Thailand",
    "Timor-Leste", "East Timor",
    "Togo",
    "Tokelau",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Türkiye", "Turkey",
    "Turkmenistan",
    "Turks and Caicos Islands",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates", "UAE",
    "United Republic of Tanzania", "Tanzania",
    "United Kingdom of Great Britain and Northern Ireland", "United Kingdom", "UK", "Great Britain", "GB",
    "United States of America", "United States", "USA", "US", "America",
    "United States Virgin Islands", "US Virgin Islands",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Venezuela (Bolivarian Republic of)", "Venezuela",
    "Viet Nam", "Vietnam",
    "Wallis and Futuna",
    "Yemen",
    "Zambia",
    "Zimbabwe"
]
codes = df_who['Country_code'].unique().tolist()
countries += codes

# Extract the date from the 'created_at' column
df['date'] = pd.to_datetime(df['created_at']).dt.date

# Function to extract the amount of deaths from the original_text column
def extract_deaths(text):
    # Try to find the pattern "number + any characters + deaths"
    match = re.search(r'deaths?\D{0,30}(\d+)', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # If not found, try to find the pattern "deaths + any characters + number"
    match = re.search(r'(\d+)\D{0,30}deaths?', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    return None

# Function to extract the country name from the original_text column
def extract_country(text):
    for country in countries:
        try:
            if country in text:
                return country
        except:
            return None
    return None
def extract_country_from_place(place):
    for country in countries:
        try:
            if country in place:
                return country
        except:
            return None
    return None
def extract_country_combined(row):
    country_from_text = extract_country(row['original_text'])
    if country_from_text:
        return country_from_text
    else:
        return extract_country_from_place(row['place'])

substrings = ['covid19', 'covid-19', 'covid 19', 'CV19', 'COVID_19',',','.']
pattern = '|'.join(re.escape(sub) for sub in substrings)
df['original_text'] = df['original_text'].str.replace(pattern, '', flags=re.IGNORECASE)

df['amount_of_deaths'] = df['original_text'].apply(extract_deaths)
df['country'] = df.apply(lambda row: extract_country_combined(row), axis=1)

df = df.dropna(subset=['amount_of_deaths', 'country'])

# Display the DataFrame with the new columns
output_file = 'extracted_deaths_info.csv'

df[['original_text', 'amount_of_deaths', 'date', 'country']].to_csv(output_file, index=True)
