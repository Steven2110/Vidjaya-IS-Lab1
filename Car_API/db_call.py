import json
import os
from Car_API import db_key as key
from pymongo import MongoClient


# Connect to MongoDB database
cluster = MongoClient(key.API_KEY)

# Select the database cluster
db = cluster["IS"]

# Select the data collection from the cluster
collection = db["CarData"]

# Car profile category = Economic, Family, Sport, Mini, Spacious, Status


def get_queries_logic_match_car(user_want):
    logic = {}

    # Logic for car with min <= price <= max. min, max are from user input
    logic["price"] = {"$gte": user_want["min_price"],
                      "$lte": user_want["max_price"]}

    # Logic for car with Vehicle Style equal to the Vehicle Style that the user want
    if user_want["body_type"][0] != "Any":
        logic["vehicle_style"] = {"$in": user_want["body_type"]}

    # Logic for car with Fuel type equal to the Fuel type that the user want
    if user_want["fuel_type"][0] != "Any":
        logic["engine_fuel_type"] = {"$in": user_want["fuel_type"]}

    # Logic for car with Transmission type equal to the Transmission type that the user want
    if user_want["transmission_type"][0] != "Any":
        if "Automatic" in user_want["transmission_type"]:
            user_want["transmission_type"].append("Automated manual")
        logic["transmission_type"] = {"$in": user_want["transmission_type"]}

    # Logic for car with Color equal to the Color that the user want
    if user_want["color"][0] != "Any":
        logic["color"] = {"$in": user_want["color"]}

    # Logic for car with Brand equal to the Brand that the user want
    if user_want["brand"][0] != "Any":
        logic["make"] = {"$in": user_want["brand"]}

    # Logic for car with Size equal to the Size that the user want
    if user_want["vehicle_size"][0] != "Any":
        logic["vehicle_size"] = {"$in": user_want["vehicle_size"]}

    # Logic for car with Production year equal to the Production year that the user want
    if user_want["minimum_year"] != "Any":
        logic["year"] = {"$gte": user_want["minimum_year"]}

    # Logic for car with the market category/class are in the profile that the user want
    if user_want["profile"] != "Any":
        # Base knowledge:
        # Car profile:
        # 1. Family: Car with class/market category "C", "D" and "J"
        # 2. Status: Car with class/market category "E", "F" and "S"
        # 3. Sport: Car with class/market category "S"
        # 4. Mini: Car with class/market category "A" and "B"
        # 5. Spacious: Car with class/market category "D", "E", "F" and "J"
        # 6. Economic: If car fuel== "Petrol" and "Diesel": City KPL >= 10.8
        #              If car fuel== "Hybrid": City KPL >= 21.26
        #              If car fuel== "Electric": City KPL >= 42.51
        family = ["C", "D", "J"]
        status = ["E", "F", "S"]
        sport = ["S"]
        mini = ["A", "B"]
        spacious = ["D", "E", "F", "J"]

        categories = []

        # Find the matching car class for each profile that the user want
        if "Family" in user_want["profile"]:
            for i in family:
                if i not in categories:
                    categories.append(i)
        if "Status" in user_want["profile"]:
            for i in status:
                if i not in categories:
                    categories.append(i)
        if "Sport" in user_want["profile"]:
            for i in sport:
                if i not in categories:
                    categories.append(i)
        if "Mini" in user_want["profile"]:
            for i in mini:
                if i not in categories:
                    categories.append(i)
        if "Spacious" in user_want["profile"]:
            for i in spacious:
                if i not in categories:
                    categories.append(i)
        if categories:
            logic["market_category"] = {"$in": categories}

        if "Economic" in user_want["profile"]:
            logic["$expr"] = {
                "$cond": {
                    "if": {"$or": [{"engine_fuel_type": "Petrol"}, {"engine_fuel_type": "Diesel"}]},
                    "then": {"$gte": ["$city_kpl", 10.8]},
                    "else": {
                        "$cond": {
                            "if": {"engine_fuel_type": "Hybrid"},
                            "then": {"$gte": ["$city_kpl", 21.26]},
                            "else": {"$gte": ["$city_kpl", 42.51]}
                        }
                    }
                }
            }
    return logic


def get_matching_car(user_want):
    best_match = []

    # Get the queries logic of every car that satisfy every characteristic that the user want
    queries_logic = get_queries_logic_match_car(user_want)
    # Get the results of the queries from the data collection
    # To get the queries result without ID Object
    results = collection.find(queries_logic, {"_id": 0})

    # Add all the queries results to the best matching car list
    for res in results:
        best_match.append(res)

    return best_match


def get_queries_logic_close_car(user_want):
    # Base knowledge: Find other car that satisfy
    # price, style, fuel type, transmission, size, profile, and production year
    # that the user want. Ignoring whatever brand or color of the car.
    logic = {}

    # Logic for car with min <= price <= max. min, max are from user input
    logic["price"] = {"$gte": user_want["min_price"],
                      "$lte": user_want["max_price"]}

    # Logic for car with ehicle Style equal to the ehicle Style that the user want
    if user_want["body_type"][0] != "Any":
        logic["vehicle_style"] = {"$in": user_want["body_type"]}

    # Logic for car with Fuel Type equal to the Fuel Type that the user want
    if user_want["fuel_type"][0] != "Any":
        logic["engine_fuel_type"] = {"$in": user_want["fuel_type"]}

    # Logic for car with Transmission Type equal to the Transmission Type that the user want
    if user_want["transmission_type"][0] != "Any":
        if "Electric" in user_want["fuel_type"]:
            user_want["transmission_type"].append("Direct drive")
        if "Automatic" in user_want["transmission_type"]:
            if "Automated manual" not in user_want["transmission_type"]:
                user_want["transmission_type"].append("Automated manual")
        logic["transmission_type"] = {"$in": user_want["transmission_type"]}

    # Logic for car with Size equal to the Size that the user want
    if user_want["vehicle_size"][0] != "Any":
        logic["vehicle_size"] = {"$in": user_want["vehicle_size"]}

    # Logic for car with Production year equal to the Production year that the user want
    if user_want["minimum_year"] != "Any":
        logic["year"] = {"$gte": user_want["minimum_year"]}

    # Logic for car with the market category/class are in the profile that the user want
    if user_want["profile"] != "Any":
        # Base knowledge:
        # Car profile:
        # 1. Family: Car with class/market category "C", "D" and "J"
        # 2. Status: Car with class/market category "E", "F" and "S"
        # 3. Sport: Car with class/market category "S"
        # 4. Mini: Car with class/market category "A" and "B"
        # 5. Spacious: Car with class/market category "D", "E", "F" and "J"
        # 6. Economic: If car fuel== "Petrol" and "Diesel": City KPL >= 10.8
        #              If car fuel== "Hybrid": City KPL >= 21.26
        #              If car fuel== "Electric": City KPL >= 42.51
        family = ["C", "D", "J"]
        status = ["E", "F", "S"]
        sport = ["S"]
        mini = ["A", "B"]
        spacious = ["D", "E", "F", "J"]

        categories = []

        # Find the matching car class for each profile that the user want
        if "Family" in user_want["profile"]:
            for i in family:
                if i not in categories:
                    categories.append(i)
        if "Status" in user_want["profile"]:
            for i in status:
                if i not in categories:
                    categories.append(i)
        if "Sport" in user_want["profile"]:
            for i in sport:
                if i not in categories:
                    categories.append(i)
        if "Mini" in user_want["profile"]:
            for i in mini:
                if i not in categories:
                    categories.append(i)
        if "Spacious" in user_want["profile"]:
            for i in spacious:
                if i not in categories:
                    categories.append(i)
        if categories:
            logic["market_category"] = {"$in": categories}

        if "Economic" in user_want["profile"]:
            logic["$expr"] = {
                "$cond": {
                    "if": {"$or": [{"engine_fuel_type": "Petrol"}, {"engine_fuel_type": "Diesel"}]},
                    "then": {"$gte": ["$city_kpl", 10.8]},
                    "else": {
                        "$cond": {
                            "if": {"engine_fuel_type": "Hybrid"},
                            "then": {"$gte": ["$city_kpl", 21.26]},
                            "else": {"$gte": ["$city_kpl", 42.51]}
                        }
                    }
                }
            }

    return logic


def get_close_car(best_match, user_want):
    close_match = []
    match = []

    # Get the queries logic of every car that satisfy some characteristic that the user want
    queries_logic = get_queries_logic_close_car(user_want)
    # Get the results of queries from the data collection
    # To get the queries result without ID Object
    results = collection.find(queries_logic, {"_id": 0})

    # Add all the results to the match list
    for res in results:
        match.append(res)

    # Removing cars that already exist in the best matching car list
    close_match = [x for x in match if x not in best_match]

    return close_match


# For testing
def test():
    user_want = {
        "min_price": 3000000,
        "max_price": 5000000,
        "body_type": ["Sedan", "SUV"],
        "fuel_type": ["Petrol"],
        "transmission_type": ["Manual", "Automatic"],
        "color": ["Black", "Red"],
        "brand": ["BMW", "Mercedes-Benz", "Mazda", "Honda", "Kia"],
        "minimum_year": 2015,
        "vehicle_size": ["Midsize"],
        "profile": ["Economic"]
    }
    res = get_matching_car(user_want)
    res2 = get_close_car(res, user_want)
    cwd = os.getcwd()
    file = open(cwd + "/Car_API/Test_Result_File/test_query_best.txt", "w")
    file2 = open(cwd + "/Car_API/Test_Result_File/test_query_close.txt", "w")
    file.write("Best match\n")
    file.write(f"Total {len(res)} best match found!\n")
    for item in res:
        file.write(str(json.dumps(item, indent=4))+'\n')
    file2.write("Close match\n")
    file2.write(f"Total {len(res2)} close match found!\n")
    for item in res2:
        file2.write(str(json.dumps(item, indent=4))+'\n')
    file.close()
    file2.close()

# test()