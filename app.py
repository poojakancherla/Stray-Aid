from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import requests
from flask_googlemaps import GoogleMaps, Map



app = Flask(__name__)

cred = credentials.Certificate("animals-a662f-firebase-adminsdk-29wae-4cd84b0745.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
animals_data = db.collection(u'animals')

# @app.route('/')
# def map_func():
# 	return render_template('map.html',apikey=api_key,latitude=latitude,longitude=longitude)#map.html is my HTML file name

# @app.route('/drinks')
# def get_drinks():    
#     drinks = [drink.to_dict() for drink in drink_data.get()]
#     return jsonify(drinks), 200

# @app.route('/drinks/<name>')
# def get_drink(name):
#     drinks = [drink.to_dict() for drink in drink_data.get()]
#     for drink in drinks:
#         if drink['name'] == name:
#             return drink
#     return "Drink not found"   

# @app.route('/drinks', methods=['POST'])
# def add_drink():
#     drink_data.add({'name': request.json['name'], 'description': request.json['description']})
#     return {"message":"added drink"}

# @app.route('/drinks/delete/<name>')
# def del_drink(name):
#     drink = request.args.get(name)
#     drink_data.document(drink).delete()
#     return {"message" : "drink deleted"}

# api_key = "AIzaSyCcHTOdNeHwZ91F_C8e9ToQoVnpXn_D9Ag" # change this to your api key
# # get api key from Google API Console (https://console.cloud.google.com/apis/)
# GoogleMaps(app, key=api_key) # set api_key


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        name = request.form.get('name')
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        animals_data.document(str(len(list(animals_data.get())) + 1)).set(({'name': name, 'lat': lat, 'lng':lng}))
    
    animals = []
    animals = [x.to_dict() for x in list(animals_data.get())]
    return render_template('geolocation.html', animals=animals) # render template

# def add_drink():
#     drink_data.add({'name': request.json['name'], 'description': request.json['description']})

@app.route('/getdata', methods=['GET', 'POST'])
def getdata():
    json_data = requests.get.args('json')
    return json_data
    # you can use this to get request with strings and parse json
    # put data in database or something

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)