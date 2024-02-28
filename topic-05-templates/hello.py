from flask import Flask, jsonify, send_from_directory, render_template
import json
from mongita import MongitaClientDisk

# open a mongita client connection
client = MongitaClientDisk()

# open a movie database
movie_db = client.movie_db

app = Flask(__name__)

@app.route("/data/movies/scifi")
def get_data_movies_scifi():
    #with open("classic_sci_fi_movies.json", "r") as f:
    #    data = json.load(f)
    # open a scifi collection
    scifi_collection = movie_db.scifi_collection
    data = list(scifi_collection.find({}))
    for item in data:
        del item["_id"]
    return jsonify(data)

@app.route('/')
def serve_index():
    return send_from_directory('.', "index.html")

# allows us to change information in the template based on given variables
@app.route("/hello")
@app.route("/hello/<name>")
def get_hello(name="stranger"):
    return render_template("hello.html", names=[name,"Alpha","Beta","Gamma"])

@app.route("/movies")
@app.route("/movies/<keyword>")
def get_movies(keyword=None):
    scifi_collection = movie_db.scifi_collection
    data = list(scifi_collection.find({}))
    for item in data:
        del item["_id"]
    if keyword:
        data = [item for item in data if keyword in item['plot']]
    return render_template("movies.html", movies=data)

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)