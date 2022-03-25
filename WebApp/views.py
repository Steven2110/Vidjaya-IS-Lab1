from flask import Blueprint, render_template, request, flash, redirect, url_for
from Car_API import api
import json

views = Blueprint('views', __name__)

user_want = {
        "min_price": 1000000,
        "max_price": 50000000,
        "body_type": ["Any"],
        "fuel_type": ["Any"],
        "transmission_type": ["Any"],
        "color": ["Any"],
        "brand": ["Any"],
        "minimum_year": 2015,
        "vehicle_size": ["Any"],
        "profile": ["Any"]
}

@views.route('/')
def home():
    return render_template("/index.html")

@views.route('/price', methods=["POST", "GET"])
def price():
    return render_template("/html/minmaxprice.html")

@views.route('/type', methods=["POST", "GET"])
def type():
    if request.method == 'POST':
        min_price = request.form.get('minprice')
        max_price = request.form.get('maxprice')
        if min_price != "0":
            user_want["min_price"] = int(min_price)
        if max_price != "0":
            user_want["max_price"] = int(max_price)
    return render_template("/html/bodytype.html")

@views.route('/fuel', methods=["POST", "GET"])
def fuel():
    if request.method == 'POST':
        body_types = request.form.getlist('input_body')
        if body_types != []:
            if "Any" not in body_types:
                user_want["body_type"] = [x for x in body_types]
    return render_template("/html/fueltype.html")

@views.route('/transmission', methods=["POST", "GET"])
def transmission():
    if request.method == 'POST':
        fuel_types = request.form.getlist('input_fuel')
        if fuel_types != []:
            if "Any" not in fuel_types:
                user_want["fuel_type"] = [x for x in fuel_types]
    return render_template("/html/transmissiontype.html")

@views.route('/brand', methods=["POST", "GET"])
def brand():
    if request.method == 'POST':
        transmissions = request.form.getlist('input_transmission')
        if transmissions != []:
            if "Any" not in transmissions:
                user_want["transmission_type"] = [x for x in transmissions]
    return render_template("/html/brand.html")

@views.route('/color', methods=["POST", "GET"])
def color():
    if request.method == 'POST':
        brands = request.form.getlist('input_brand')
        if brands != []:
            if "Any" not in brands:
                user_want["brand"] = [x for x in brands]
    return render_template("/html/colortype.html")


@views.route('/year', methods=["POST", "GET"])
def year():
    if request.method == 'POST':
        colors = request.form.getlist('input_color')
        if colors != []:
            if "Any" not in colors:
                user_want["color"] = [x for x in colors]
    return render_template("/html/minimumyear.html")

@views.route('/size', methods=["POST", "GET"])
def size():
    if request.method == 'POST':
        year = request.form.get('input_year')
        if year != "Any":
            user_want["minimum_year"] = int(year)
    return render_template("/html/vehiclesize.html")

@views.route('/profile', methods=["POST", "GET"])
def profile():
    if request.method == 'POST':
        sizes = request.form.getlist('input_size')
        if sizes != "Any":
            user_want["vehicle_size"] = [x for x in sizes]
    return render_template("/html/carprofile.html")

@views.route('/result', methods=["POST", "GET"])
def result():
    if request.method == 'POST':
        profiles = request.form.getlist('input_profile')
        if profiles != "Any":
            user_want["profile"] = [x for x in profiles]
        file1 = open("test.txt", "w")
        file1.write(str(json.dumps(user_want, indent=4)))
        file1.close()
        print(user_want)
        car = api.IntelligenceSystemCar(user_want)
        best_match = car.get_best_match()
        close_match = car.get_close_match(best_match)
        file2 = open("test_result.txt", "w")
        for match in best_match:
            file2.write(str(json.dumps(match, indent=4)) + '\n')
        file2.close()
        # all_match = {
        #     "best_match": [],
        #     "close_match": []
        # }
        # all_match["best_match"] = best_match
        # all_match["close_match"] = close_match
    return render_template("/html/result.html", data1=best_match, data2=close_match)

