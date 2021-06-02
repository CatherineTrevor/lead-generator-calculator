import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
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
    return render_template("index.html")


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
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for(
                    "account", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("log_in"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
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
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username")
        return redirect(url_for("account", username=session["user"]))
    return render_template("sign_up.html")


@app.route("/account_profile")
def get_account_profile():
    accounts = list(mongo.db.accounts.find())
    campaigns = list(mongo.db.campaigns.find())
    calculations = list(mongo.db.calculations.find())
    return render_template("account.html",
                            accounts=accounts, campaigns=campaigns,
                            calculations=calculations)


@app.route("/account<username>", methods=["GET", "POST"])
def account(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session['user']:
        return redirect(url_for("get_account_profile"))

    return redirect(url_for("log_in"))


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/create_campaign", methods=["GET", "POST"])
def create_campaign():
    if request.method == "POST":
        campaign = {
            "campaign_name": request.form.get("campaign_name"),
            "campaign_type": request.form.get("campaign_type"),
            "communication_platform": request.form.get(
                "communication_platform"),
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date"),
            "marketing_qualified_leads": request.form.get(
                "marketing_qualified_leads"),
            "sales_qualified_leads": request.form.get(
                "sales_qualified_leads"),
            "total_campaign_cost": request.form.get("total_campaign_cost"),
            "owning_account": session["user"]
        }
        mongo.db.campaigns.insert_one(campaign)
        calculate_results()
        flash("Task succesfully added")
        return redirect(url_for("get_account_profile"))

    return render_template("create_campaign.html")


@app.route("/calculate", methods=["GET", "POST"])
def calculate_results():
    if request.method == "POST":

        total_campaign_cost = int(request.form.get("total_campaign_cost"))
        mql = int(request.form.get("marketing_qualified_leads"))
        sql = int(request.form.get("sales_qualified_leads"))
        calc_cost_mql = int(total_campaign_cost / mql)
        calc_cost_sql = int(total_campaign_cost / sql)
        calc_hit_rate = int(sql / mql * 100)

        calculation = {
            "owning_account": session["user"],
            "campaign_name": request.form.get("campaign_name"),
            "marketing_qualified_leads": request.form.get(
                "marketing_qualified_leads"),
            "sales_qualified_leads": request.form.get(
                "sales_qualified_leads"),
            "cost_per_marketing_lead": calc_cost_mql,
            "cost_per_sales_lead": calc_cost_sql,
            "hit_rate": calc_hit_rate
        }
        mongo.db.calculations.insert_one(calculation)
        return redirect(url_for("get_account_profile"))

    calculations = mongo.db.calculations.find()
    return render_template('account.html', calculations=calculations)


@app.route("/delete_campaign/<campaign_id>")
def delete_campaign(campaign_id):
    mongo.db.campaigns.remove({"_id": ObjectId(campaign_id)})
    flash("Task deleted")
    return redirect(url_for("get_account_profile"))


@app.route("/log_out")
def log_out():
    # remove user from session cookies
    flash("You have been logged out")
    # can also use session.clear()
    session.pop("user")
    return redirect(url_for("log_in"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
