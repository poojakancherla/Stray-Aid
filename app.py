from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import requests
from flask_googlemaps import GoogleMaps

app = Flask(__name__)

cred = credentials.Certificate("animals-a662f-firebase-adminsdk-29wae-4cd84b0745.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
animals_data = db.collection(u'animals')

api_key = "AIzaSyCQvpfaUvYtqZLU1UP__Uq1OrqJB5_8Fz0" 
GoogleMaps(app, key=api_key) 

def get_address(lat, lng):
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lng) + "&key=" + api_key
    response = requests.get(url).json() 
    address = ""
    response.keys()
    if response['status'] == 'OK':
        address = response["results"][0]["formatted_address"]
    return address
    
def populate_data(animals_data):
    animals = []
    for animal in animals_data.get():
        animal = animal.to_dict()
        name, lat, lng = animal["name"], animal["lat"], animal["lng"]
        address = get_address(lat, lng)
        d = {"name":name, "address":address}
        animals.append(d)
    return animals

def add_data(name, lat, lng):
    animals_data.document(str(len(list(animals_data.get())) + 1)).set(({'name': name, 'lat': lat, 'lng':lng}))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        name = request.form.get('name')
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        add_data(name, lat, lng)
    return render_template('geolocation.html', animals=populate_data(animals_data)) # render template

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)