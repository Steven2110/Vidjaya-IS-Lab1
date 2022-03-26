from pymongo import MongoClient
import csv
import json
import os
from db_key import API_KEY as key

# Connect to MongoDB database
cluster = MongoClient(key)

# Select the database cluster
db = cluster["IS"]

# Select the data collection from the cluster
collection = db["CarData"]

# To return all data from DB without its id object


def get_current_data():
    return collection.find({}, {"_id": 0})


def insert_data():
    print("Inputing data....")

    # Get all data from DB, for comparison later
    current_data_db = get_current_data()
    current_data = []
    for item in current_data_db:
        current_data.append(item)

    # CSV to JSON conversion
    cwd = os.getcwd()
    csvfile = open(cwd + "/Data/data_placeholder.csv", "r")
    reader = csv.DictReader(csvfile)

    headers = ["make", "model", "year", "color", "engine_fuel_type", "engine_hp", "engine_cylinders", "transmission_type",
               "driven_wheels", "number_of_doors", "market_category", "vehicle_size", "vehicle_style", "city_kpl", "price"]

    counter = 0
    uninserted_counter = 0
    uninserted_data = []

    for each in reader:
        print()
        data = {}
        for field in headers:
            data[field] = each[field]
        if data not in current_data:
            collection.insert_one(data)
            counter += 1
        else:
            uninserted_data.append(data)
            uninserted_counter += 1

    print(f"{counter} data have successfully been inserted!")
    if uninserted_data != []:
        for uninserted in uninserted_data:
            print(json.dumps(uninserted, indent=4))
        print(
            f"{uninserted_counter} data already in the database, consider updating them!")

    csvfile.close()

# To insert data please fill in the file 'data_placeholder.xlsx' in 'Data' folder.
# Then convert the file to .csv file with the same name replace the existing file
# Return to this file and run the file, then you can see from the console the progress of inserting data to database


insert_data()
