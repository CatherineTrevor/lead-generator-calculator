import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/benchmark_data")
def benchmark_data():
    return render_template("benchmark_data.html")


@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})
        if existing_user:
            return redirect(url_for(
                23"account", username=session["user"]))
        else:
            return redirect(url_for("log_in"))

    return render_template("log_in.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # check if username exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("sign_up"))

        register = {
            "username": request.form.get("username"),
            "password": request.form.get("password")
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username")
        return redirect(url_for("account", username=session["user"]))
    return render_template("sign_up.html")


@app.route("/account")
def account():
    return render_template("account.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/create_campaign")
def create_campaign():
    return render_template("create_campaign.html")


@app.route("/create_category")
def create_category():
    return render_template("create_category.html")


@app.route("/log_out")
def log_out():
    return redirect(url_for("log_in"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)