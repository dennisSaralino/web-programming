from flask import Flask, render_template, request, redirect # redirect
from mongita import MongitaClientDisk
from bson import ObjectId

app = Flask(__name__)

# open a mongita client connection
client = MongitaClientDisk()

# open a quote database
quotes_db = client.quotes_db

# GET method
@app.route("/", methods=["GET"])
@app.route("/quotes", methods=["GET"])
def get_quotes():
    quotes_collection = quotes_db.quotes_collection
    data = list(quotes_collection.find({}))
    for item in data:
        item["_id"] = str(item["_id"])
        item["object"] = ObjectId(item["_id"])
    print(data)
    return render_template("quotes.html", data=data)


@app.route("/create", methods=["GET"])
def get_create():
    return render_template("create.html")

@app.route("/create", methods=["POST"])
def post_create():
    quotes_collection = quotes_db.quotes_collection
    quote = request.form.get("quote", None)
    author = request.form.get("author", None)
    quotes_collection.insert_one({"text": quote, "author": author})
    return redirect("/quotes")

@app.route("/edit", methods=["GET"])
@app.route("/edit/<id>", methods=["GET"])
def get_edit(id=None):
    if id:
        return render_template("edit.html", id=id)
    return redirect("/quotes")

@app.route("/post_edit", methods=["POST"])
@app.route("/post_edit/<id>", methods=["POST"])
def post_edit(id=None):
    if id:
        quotes_collection = quotes_db.quotes_collection
        newQuote = request.form.get("newQuote", None)
        newAuthor = request.form.get("newAuthor", None)
        data = {
            'text': newQuote,
            'author': newAuthor
        }
        quotes_collection.update_one({"_id":ObjectId(id)}, data)
    return redirect("/quotes")


@app.route("/delete", methods=["GET"])
@app.route("/delete/<id>", methods=["GET"])
def get_delete(id=None):
    if id:
        # open the quotes collection
        quotes_collection = quotes_db.quotes_collection
        #delete the item
        quotes_collection.delete_one({"_id":ObjectId(id)})
    return redirect("/quotes")
