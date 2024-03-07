from flask import Flask, render_template, request # redirect
from mongita import MongitaClientDisk

# open a mongita client connection
client = MongitaClientDisk()

# open a quote database
quotes_db = client.quotes_db

app = Flask(__name__)

# pulls info from URL parameters from form

# GET method
@app.route("/", methods=["GET"])
@app.route("/quotes", methods=["GET"])
def get_quotes():
    quotes_collection = quotes_db.quotes_collection
    data = list(quotes_collection.find({}))
    for item in data:
        item["_id"] = str(item["_id"])
    print(data)
    return render_template("quotes.html", data=data)

@app.route("/delete", methods=["GET"])
@app.route("/delete/<id>", methods=["GET"])
def get_delete(id=None):
    if id:
        # open the quotes collection
        quotes_collection = quotes_db.quotes_collection
        #delete the item
        quotes_collection.delete_one({'_id'==id})
