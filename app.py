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
        existing_user = mongo.db.accounts.find_one(
            {"email_address": request.form.get("email_address").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("email_address").lower()
                return redirect(url_for(
                    "account", email_address=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("log_in"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("log_in"))

    return render_template("log_in.html")


@app.route("/log_out")
def log_out():
    # remove user from session cookies
    flash("See you again soon!")
    # can also use session.clear()
    session.pop("user")
    return redirect(url_for("log_in"))


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # check if username exists in database
        existing_user = mongo.db.accounts.find_one(
            {"email_address": request.form.get("email_address")})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("sign_up"))

        register = {
            "email_address": request.form.get("email_address"),
            "password": generate_password_hash(request.form.get("password")),
            "company_name": "Enter your company name",
            "account_owner": "Please update your details!",
            "company_country_name": "Select your country",
            "company_industry": "Select your industry",
            "currency": "Your currency"
        }
        mongo.db.accounts.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("email_address")
        return redirect(url_for("account", email_address=session["user"]))
    return render_template("sign_up.html")


@app.route("/account_profile")
def get_account_profile():
    accounts = list(mongo.db.accounts.find())
    campaigns = list(mongo.db.campaigns.find())
    calculations = list(mongo.db.calculations.find())
    return render_template("account.html",
                            accounts=accounts, campaigns=campaigns,
                            calculations=calculations)


@app.route("/account<email_address>", methods=["GET", "POST"])
def account(email_address):
    # grab the session user's username from db
    email_address = mongo.db.accounts.find_one(
        {"email_address": session["user"]})["email_address"]

    if session['user']:
        return redirect(url_for("get_account_profile"))

    return redirect(url_for("log_in"))


@app.route("/account_update/<account_id>", methods=["GET", "POST"])
def account_update(account_id):
    if request.method == "POST":
        submit = {
            "company_name": request.form.get("company_name"),
            "account_owner": request.form.get("account_owner"),
            "company_country_name": request.form.get("company_country_name"),
            "company_industry": request.form.get("company_industry"),
            "currency": request.form.get("currency"),
            "password": session["user"],
            "email_address": session["user"]
        }
        mongo.db.accounts.update({"_id": ObjectId(account_id)}, submit)
        flash("Account successfully updated")
        return redirect(url_for("get_account_profile"))

    account = mongo.db.accounts.find_one({"_id": ObjectId(account_id)})

    return render_template("account_update.html", account=account)


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


@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    if request.method == "POST":
        message = {
            "contact_name": request.form.get("contact_name"),
            "company_name": request.form.get("company_name"),
            "email_address": request.form.get("email_address"),
            "phone_number": request.form.get("phone_numer"),
            "message": request.form.get("message"),
        }
        mongo.db.contacts.insert_one(message)
        flash("We have received your message")
        return redirect(url_for("contact_us"))

    return render_template("contact_us.html")


@app.route("/admin")
def admin():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("admin.html", categories=categories) 


@app.route("/create_category", methods=["GET", "POST"])
def create_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name"),
            "category_type": request.form.get("category_type"),
        }
        mongo.db.categories.insert_one(category)
        flash("Category succesfully added")
        return redirect(url_for("admin"))

    return render_template("create_category.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
