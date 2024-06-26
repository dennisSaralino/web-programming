from flask import Flask, render_template, request, redirect, make_response
from mongita import MongitaClientDisk
from bson import ObjectId

app = Flask(__name__)

# open a mongita client connection
client = MongitaClientDisk()

# open a quote database
quotes_db = client.quotes_db

import uuid

# Generate a random UUID
session_key = uuid.uuid4()
print(session_key)

# GET method
@app.route("/", methods=["GET"])
@app.route("/quotes", methods=["GET"])
def get_quotes():
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return("You are not logged in.")
        session_id = str(uuid.uuid4())
    number_of_visits = int(request.cookies.get("number_of_visits", "0"))
    quotes_collection = quotes_db.quotes_collection
    data = list(quotes_collection.find({}))
    for item in data:
        item["_id"] = str(item["_id"])
        item["object"] = ObjectId(item["_id"])
    print(data)
    html = render_template("quotes.html", data=data,
    number_of_visits=number_of_visits, session_id=session_id, user=user)
    response = make_response(html)
    response.set_cookie("number_of_visits", str(number_of_visits + 1))
    response.set_cookie("session_id", session_id)
    return response

# Automatic login page
@app.route("/login", methods=["GET"])
def get_login():
    session_id = request.cookies.get("session_id", None)
    if session_id:
        response = redirect("/quotes")
        return response
    return render_template("login.html")
    

# Form-based login page
app.route("/login", methods=["POST"])
def post_login():
    response = redirect("/quotes")
    session_id = str(uuid.uuid4())
    response.set_cookie("session_id", session_id)
    user = request.form.get("user", "")
    response.set_cookie("user", user)
    return response

@app.route("/logout", methods=["GET"])
def get_logout():
    response = redirect("/login")
    response.delete_cookie("session_id")
    return response

@app.route("/create", methods=["GET"])
def get_create():
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return("You are not logged in.")
    return render_template("create.html")

@app.route("/create", methods=["POST"])
def post_create():
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return("You are not logged in.")
    quotes_collection = quotes_db.quotes_collection
    quote = request.form.get("quote", None)
    author = request.form.get("author", None)
    quotes_collection.insert_one({"text": quote, "author": author})
    return redirect("/quotes")

@app.route("/edit/<id>", methods=["GET"])
def get_edit(id=None):
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return("You are not logged in.")
    if id:
        # open the quotes collection
        quotes_collection = quotes_db.quotes_collection
        # get the item
        data = quotes_collection.find_one({"_id": ObjectId(id)})
        data["id"] = str(data["_id"])
        return render_template("edit.html", data=data)
    return redirect("/quotes")

@app.route("/edit", methods=["POST"])
def post_edit():
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return("You are not logged in.")
    _id = request.form.get("_id", None)
    text = request.form.get("newQuote", "")
    author = request.form.get("newAuthor", "")
    if _id:
        # open the quotes collection
        quotes_collection = quotes_db.quotes_collection
        # update the values in this particular record
        values = {"$set": {"text": text, "author": author}}
        data = quotes_collection.update_one({"_id": ObjectId(_id)}, values)
    return redirect("/quotes")


@app.route("/delete", methods=["GET"])
@app.route("/delete/<id>", methods=["GET"])
def get_delete(id=None):
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        return("You are not logged in.")
    if id:
        # open the quotes collection
        quotes_collection = quotes_db.quotes_collection
        #delete the item
        quotes_collection.delete_one({"_id":ObjectId(id)})
    return redirect("/quotes")
