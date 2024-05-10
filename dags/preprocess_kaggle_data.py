import csv


def preprocess_kaggle_data(file_name):
    path = '../datasets/tweets/'
    # Open the CSV file for reading and a new file for writing the cleaned data
    with open(f'{path}{file_name}', 'r', encoding='utf-8') as csv_file, open(f'{path}/clean_{file_name}', 'w', encoding='utf-8',
                                                                        newline='') as cleaned_file:
        reader = csv.reader(csv_file)
        writer = csv.writer(cleaned_file)

        header = next(reader)
        writer.writerow(header)

        for row in reader:

            row[3] = row[3].replace('\n', ' ')

            writer.writerow(row)


if __name__ == '__main__':
    preprocess_kaggle_data('tw-1.csv')
    preprocess_kaggle_data('tw-2.csv')
    preprocess_kaggle_data('tw-3.csv')
