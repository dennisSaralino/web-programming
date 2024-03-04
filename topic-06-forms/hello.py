from flask import Flask, render_template, request

app = Flask(__name__)

# pulls info from URL parameters from form

# GET method
@app.route("/hello", methods=["GET"])
def get_hello():
    
    #name = request.args.get("name", None)
    #password = request.args.get("password", None)
    #print([name, password])
    data = {
        "name": None,
        "password": None
    }
    return render_template("hello.html", data=data)

# POST method
@app.route("/hello", methods=["POST"])
def post_hello():
    name = request.form.get("name", None)
    password = request.form.get("password", None)
    print([name, password])
    data = {
        "name": name,
        "password": password
    }
    return render_template("hello.html", data=data)