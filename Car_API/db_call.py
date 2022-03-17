import json
import os
from textwrap import indent

from numpy import true_divide
from db_key import API_KEY
from pymongo import MongoClient
from sort import mergeSort

cluster = MongoClient(API_KEY)
db = cluster["IS"]
collection = db["CarData"]

# Economic, Family, Sport, Mini, Spacious, Status
# user_want = {
#     "min_price": 3000000,
#     "max_price": 5000000,
#     "body_type": ["Sedan", "SUV"],
#     "fuel_type": ["Petrol"],
#     "transmission_type": ["Manual", "Automatic"],
#     "color": ["Black", "Red"],
#     "brand": ["BMW", "Mercedes-Benz", "Mazda", "Honda", "Kia"],
#     "minimum_year": 2015,
#     "vehicle_size": ["Midsize"],
#     "profile": ["Economic"]
# }


def get_queries_logic(user_want):
    logic = {}
    logic["Price"] = {"$gte": user_want["min_price"],
                      "$lte": user_want["max_price"]}
    if user_want["body_type"][0] != "Any":
        logic["Vehicle Style"] = {"$in": user_want["body_type"]}
    if user_want["fuel_type"][0] != "Any":
        logic["Engine Fuel Type"] = {"$in": user_want["fuel_type"]}
    if user_want["transmission_type"][0] != "Any":
        logic["Transmission Type"] = {"$in": user_want["transmission_type"]}
    if user_want["color"][0] != "Any":
        logic["Color"] = {"$in": user_want["color"]}
    if user_want["brand"][0] != "Any":
        logic["Make"] = {"$in": user_want["brand"]}
    if user_want["vehicle_size"][0] != "Any":
        logic["Vehicle Size"] = {"$in": user_want["vehicle_size"]}
    if user_want["minimum_year"] != "Any":
        logic["Year"] = {"$gte": user_want["minimum_year"]}
    print(logic)
    return logic


def get_matching_car(user_want):
    best_match = []
    queries_logic = get_queries_logic(user_want)
    results = db.CarData.find(queries_logic, {"_id": 0})
    for res in results:
        best_match.append(res)
    return best_match


# res = get_matching_car(user_want)
# cwd = os.getcwd()
# file = open(cwd + "/carAPI/test.txt", "w")

# for item in res:
#     file.write(str(json.dumps(item, indent=4)))

# file.close()
