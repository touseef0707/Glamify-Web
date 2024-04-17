import random
import csv
import json

# function to get data's from CSV files and convert it into dictionary
def getData():
    images_file_name = 'C:/Users/Hp/Dropbox/PC/Desktop/Personal/uni_west_london/sem_4/Group Research Project 2024/fashion-dataset/images.csv'
    styles_file_name = 'C:/Users/Hp/Dropbox/PC/Desktop/Personal/uni_west_london/sem_4/Group Research Project 2024/fashion-dataset/styles.csv'
    data_men = {}
    data_women = {}
    data_boys = {}
    data_girls = {}
    data_unisex = {}
    data_complete = {"Men": data_men,
                     "Women": data_women,
                     "Boys": data_boys,
                     "Girls": data_girls,
                     "Unisex": data_unisex}
    img = {}

    with open(styles_file_name, mode='r') as styles_file, open(images_file_name, mode='r') as images_file:
        csv_reader = csv.reader(styles_file)
        img_reader = csv.reader(images_file)
       
        for row in img_reader:
            num = row[0].split(".")[0]
            img[num] = row[1]

        for row in csv_reader:
           if row[0] != "id":
                gender = row[1]  
                metadata = row[2:] + [img[row[0]]]

                if gender == "Men":
                    data_men[row[0]]  = metadata

                elif gender == "Women":
                    data_women[row[0]] = metadata

                elif gender == "Boys":
                    data_boys[row[0]] = metadata

                elif gender == "Girls":
                    data_girls[row[0]] = metadata

                else:
                    data_unisex[row[0]] = metadata
    return data_complete

# function that takes in data and creates a new file with the data
def writeDataToFile(data_complete, output_file_name):
    with open(output_file_name, mode='w', newline='') as output_file:
        csv_writer = csv.writer(output_file)

        # Write header
        csv_writer.writerow(['gender', 'id', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage', 'productDisplayName', 'link'])

        # Write data from data_complete dictionary
        for gender, data in data_complete.items():
            for item_id, metadata in data.items():
                row = [gender, item_id] + metadata
                csv_writer.writerow(row)

# function to read data from the file and convert it into dictionary
def readDataFromFile(input_file_name):
    data_complete = {}
    
    with open(input_file_name, mode='r') as input_file:
        csv_reader = csv.reader(input_file)
        next(csv_reader)  # Skip the header row
        
        for row in csv_reader:
            gender = row[0]
            item_id = row[1]
            metadata = row[2:]
            
            if gender not in data_complete:
                data_complete[gender] = {}
            
            data_complete[gender][item_id] = metadata
    
    return data_complete

# Function to generate random price between 10 and 60 with two decimal places
def generate_random_price():
    return round(random.uniform(10, 60), 2)

#generate random quantity between 1 and 20
def generate_random_quantity():
    return random.randint(1, 20)

# Function that adds columns in the dataset
def add_column(input_file_name, output_file_name):

    # Read data from the input CSV file and add a new column with randomly generated prices
    with open(input_file_name, mode='r') as input_file, open(output_file_name, mode='w', newline='') as output_file:
        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)

        header = next(csv_reader)
        header.append('Quantity')
        csv_writer.writerow(header)

        # Process each row and add randomly generated price
        for row in csv_reader:
            price = generate_random_quantity()
            row.append(price)
            csv_writer.writerow(row)


# Function to convert data from CSV file to dictionary and write it to a text file
def read_csv_and_create_dictionary(csv_filename):
    # Initialize an empty dictionary to store the data
    import csv
    data_dict = {
        "Men": [],
        "Women": [],
        "Boys": [],
        "Girls": [],
        "Unisex": []
    }

    # Read data from the CSV file and populate the dictionary
    with open(csv_filename, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Create a dictionary for the current row
            item = {
                'gender': row['gender'],
                'id': row['id'],
                'masterCategory': row['masterCategory'], 
                'subCategory': row['subCategory'], 
                'articleType': row['articleType'], 
                'baseColour': row['baseColour'], 
                'season': row['season'], 
                'year': row['year'], 
                'usage': row['usage'], 
                'productDisplayName': row['productDisplayName'], 
                'link': row['link'],
                'price': row['price'],
                'quantity': row['quantity']
            }

            # Append the item to the appropriate list based on gender
            data_dict[row['gender']].append(item)

    return data_dict

def write_data_to_textfile(data, output_file):
    import json
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, indent=4))


import pandas as pd

def update_ids(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Update the 'id' column with sequential IDs starting from 1000
    df['id'] = range(1000, 1000 + len(df))
    
    # Write the updated DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)

def truncate_year(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Convert the "year" column to string and remove trailing ".0"
    df['year'] = df['year'].astype(str).str.rstrip('.0')

    # Write the updated DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)


