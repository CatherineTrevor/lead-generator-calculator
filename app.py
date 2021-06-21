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
            if check_password_hash(existing_user["password"],
                                   request.form.get("password")):
                '''
                    put the new user and password into session cookie
                    to allow for account_updates after log-in without
                    updating the password - issue #14
                '''
                session["password"] = generate_password_hash(
                                                            request.form.get("password"))
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
    session.clear()
    flash("See you again soon!")
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
        # put blank info into account until user updates it
        register = {
            "email_address": request.form.get("email_address"),
            "password": generate_password_hash(request.form.get("password")),
            "company_name": "Enter your company name",
            "account_owner": "Please update your details!",
            "company_country_name": "Enter your country",
            "company_industry": "Update your industry",
            "currency": "€"
        }
        mongo.db.accounts.insert_one(register)
        # put the new user and password into 'session' cookie
        session["user"] = request.form.get("email_address")
        session["password"] = generate_password_hash(
            request.form.get("password"))

        return redirect(url_for("account", email_address=session["user"],))
    return render_template("sign_up.html")


# Account management


@app.route("/account<email_address>", methods=["GET", "POST"])
def account(email_address):
    if session['user']:
        return redirect(url_for("get_account_profile"))

    return redirect(url_for("log_in"))


@app.route("/account_profile")
def get_account_profile():
    accounts = list(mongo.db.accounts.find())
    campaigns = list(mongo.db.campaigns.find())
    calculations = list(mongo.db.calculations.find())
    total_open_campaigns = mongo.db.campaigns.count_documents(
            {"owning_account": session['user']})
    total_marketing_spend = list(mongo.db.campaigns.aggregate([{"$match": {"owning_account": {"$eq": session['user']}}}, {"$group": {"_id": "$owning_account", "marketing_spend": {"$sum": "$total_campaign_cost"}}}]))
    total_marketing_leads = list(mongo.db.campaigns.aggregate([{"$match": {"owning_account": {"$eq": session['user']}}}, {"$group": {"_id": "$owning_account", "marketing_leads": {"$sum": "$marketing_qualified_leads"}}}]))
    total_sales_leads = list(mongo.db.campaigns.aggregate([{"$match": {"owning_account": {"$eq": session['user']}}}, {"$group": {"_id": "$owning_account", "sales_leads": {"$sum": "$sales_qualified_leads"}}}]))
    total_converted_leads = list(mongo.db.campaigns.aggregate([{"$match": {"owning_account": {"$eq": session['user']}}}, {"$group": {"_id": "$owning_account", "converted_leads": {"$sum": "$converted_leads"}}}]))
    return render_template("account.html",
                           accounts=accounts,
                           campaigns=campaigns,
                           calculations=calculations,
                           total_open_campaigns=total_open_campaigns,
                           total_marketing_spend=total_marketing_spend,
                           total_marketing_leads=total_marketing_leads,
                           total_sales_leads=total_sales_leads,
                           total_converted_leads=total_converted_leads)


@app.route("/account_update/<account_id>", methods=["GET", "POST"])
def account_update(account_id):
    if request.method == "POST":
        account = mongo.db.accounts.find_one({"_id": ObjectId(account_id)})
        calculation_id = mongo.db.calculations.find({"owning_account": session["user"]})
        campaign_id = mongo.db.campaigns.find({"owning_account": session["user"]})
        submit = {
            "email_address": session["user"],
            "password": session["password"],
            "company_name": request.form.get("company_name"),
            "account_owner": request.form.get("account_owner"),
            "company_country_name": request.form.get("company_country_name"),
            "company_industry": request.form.get("company_industry"),
            "currency": "€"
        }
        mongo.db.accounts.update({"_id": ObjectId(account_id)}, submit)
        if calculation_id:
            mongo.db.calculations.update_many({"owning_account": session["user"]}, {"$set": {"company_industry": request.form.get("company_industry")}})
            mongo.db.campaigns.update_many({"owning_account": session["user"]}, {"$set": {"company_industry": request.form.get("company_industry")}})
        flash("Account successfully updated")
        return redirect(url_for("get_account_profile"))

    account = mongo.db.accounts.find_one({"_id": ObjectId(account_id)})
    calculation_id = mongo.db.calculations.find({"owning_account": session["user"]})
    campaign_id = mongo.db.campaigns.find({"owning_account": session["user"]})
    categories = mongo.db.categories.find(
        {"category_type": "Industry"}).sort("category_name", 1)

    return render_template(
        "account_update.html", account=account, categories=categories,
        calculation_id=calculation_id, campaign_id=campaign_id)


@app.route("/delete_account/<account_id>/")
def delete_account(account_id):
    mongo.db.accounts.remove({"_id": ObjectId(account_id)})
    mongo.db.campaigns.remove({"account_id": ObjectId(account_id)})
    mongo.db.calculations.remove({"account_id": ObjectId(account_id)})
    session.clear()
    flash("Your account has been deleted")
    return redirect(url_for("sign_up"))


# Campaign management


@app.route("/create_campaign/<account_id>", methods=["GET", "POST"])
def create_campaign(account_id):
    if request.method == "POST":
        account = mongo.db.accounts.find_one({"_id": ObjectId(account_id)})
        existing_campaign_name = mongo.db.campaigns.find_one({"account_id": account["_id"], "campaign_name": {"$eq": request.form.get("campaign_name")}})
        campaign = {
            "campaign_name": request.form.get("campaign_name"),
            "campaign_type": request.form.get("campaign_type"),
            "communication_platform": request.form.get(
                "communication_platform"),
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date"),
            "marketing_qualified_leads": int(request.form.get(
                "marketing_qualified_leads")),
            "sales_qualified_leads": int(request.form.get(
                "sales_qualified_leads")),
            "converted_leads": int(request.form.get("converted_leads")),
            "total_campaign_cost": int(request.form.get("total_campaign_cost")),
            "owning_account": session["user"],
            "account_id": account["_id"],
            "company_industry": account["company_industry"]
        }
        if existing_campaign_name:
            flash("This campaign name is already in use, please use a different one")
            return redirect(url_for("create_campaign", account_id=account_id))
        mongo.db.campaigns.insert_one(campaign)
        try:
            calculate_results(account_id)
        except ValueError:
            pass
        return redirect(url_for("get_account_profile"))

    account = mongo.db.accounts.find_one({"_id": ObjectId(account_id)})
    campaign_type = mongo.db.categories.find(
        {"category_type": "Campaign type"}).sort("category_name", 1)
    communication_platform = mongo.db.categories.find(
        {"category_type": "Communication platform"}).sort("category_name", 1)
    return render_template(
        "create_campaign.html", account=account,
        campaign_type=campaign_type,
        communication_platform=communication_platform)


@app.route("/edit_campaign/<campaign_id>/<account_id>/<calculation_id>",
           methods=["GET", "POST"])
def edit_campaign(campaign_id, account_id, calculation_id):
    if request.method == "POST":
        account = mongo.db.accounts.find_one({"_id": ObjectId(account_id)})
        calculation = mongo.db.calculations.find_one({"_id": ObjectId(
            calculation_id)})
        submit = {
            "campaign_name": request.form.get("campaign_name"),
            "campaign_type": request.form.get("campaign_type"),
            "communication_platform": request.form.get(
                "communication_platform"),
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date"),
            "marketing_qualified_leads": int(request.form.get(
                "marketing_qualified_leads")),
            "sales_qualified_leads": int(request.form.get(
                "sales_qualified_leads")),
            "converted_leads": int(request.form.get("converted_leads")),
            "total_campaign_cost": int(request.form.get("total_campaign_cost")),
            "owning_account": session["user"],
            "account_id": account["_id"],
            "company_industry": account["company_industry"]
        }
        update_calculate_results(campaign_id, calculation_id)
        mongo.db.campaigns.update({"_id": ObjectId(campaign_id)}, submit)
        flash("Campaign successfully updated")
        return redirect(url_for("get_account_profile"))

    account = mongo.db.accounts.find_one({"_id": ObjectId(account_id)})
    campaign = mongo.db.campaigns.find_one({"_id": ObjectId(campaign_id)})
    calculation = mongo.db.calculations.find_one({"_id": ObjectId(
        calculation_id)})
    campaign_type = mongo.db.categories.find(
        {"category_type": "Campaign type"}).sort("category_name", 1)
    communication_platform = mongo.db.categories.find(
        {"category_type": "Communication platform"}).sort("category_name", 1)
    return render_template(
        "edit_campaign.html", account=account,
        campaign=campaign,
        campaign_type=campaign_type,
        communication_platform=communication_platform,
        calculation=calculation)


@app.route("/delete_campaign/<campaign_id>/<calculation_id>")
def delete_campaign(campaign_id, calculation_id):
    mongo.db.campaigns.remove({"_id": ObjectId(campaign_id)})
    mongo.db.calculations.remove({"_id": ObjectId(calculation_id)})
    flash("Campaign deleted")
    return redirect(url_for("get_account_profile"))


# Calculations


@app.route("/calculate/<account_id>", methods=["GET", "POST"])
def calculate_results(account_id):
    if request.method == "POST":
        total_campaign_cost = int(request.form.get("total_campaign_cost"))
        mql = int(request.form.get("marketing_qualified_leads"))
        sql = int(request.form.get("sales_qualified_leads"))
        converted_leads = int(request.form.get("converted_leads"))
        calc_cost_mql = int(total_campaign_cost / mql) if mql != 0 else 0
        calc_cost_sql = int(total_campaign_cost / sql) if sql != 0 else 0
        calc_cost_per_conversion = int(total_campaign_cost / converted_leads) if converted_leads != 0 else 0
        calc_hit_rate = int(sql / mql * 100) if mql != 0 else 0
        account = mongo.db.accounts.find_one({"_id": ObjectId(account_id)})
        campaign = mongo.db.campaigns.find_one({"_id": ObjectId()})
        calculation = {
            "owning_account": session["user"],
            "account_id": account["_id"],
            "campaign_name": request.form.get("campaign_name"),
            "company_industry": account["company_industry"],
            "marketing_qualified_leads": request.form.get(
                "marketing_qualified_leads"),
            "sales_qualified_leads": request.form.get(
                "sales_qualified_leads"),
            "cost_per_marketing_lead": calc_cost_mql,
            "cost_per_sales_lead": calc_cost_sql,
            "cost_per_converted_lead": calc_cost_per_conversion,
            "hit_rate": calc_hit_rate
        }

        mongo.db.calculations.insert_one(calculation)
        return redirect(url_for("get_account_profile"))

    calculations = mongo.db.calculations.find()
    campaign = mongo.db.campaigns.find_one({"_id": ObjectId()})
    account = mongo.db.accounts.find_one({"_id": ObjectId(account_id)})
    return render_template('account.html', calculations=calculations,
                           campaign=campaign, account=account)


@app.route("/update_calculate_results/<campaign_id>/<calculation_id>",
           methods=["GET", "POST"])
def update_calculate_results(campaign_id, calculation_id):
    if request.method == "POST":
        total_campaign_cost = int(request.form.get("total_campaign_cost"))
        mql = int(request.form.get("marketing_qualified_leads"))
        sql = int(request.form.get("sales_qualified_leads"))
        converted_leads = int(request.form.get("converted_leads"))
        calc_cost_mql = int(total_campaign_cost / mql) if mql != 0 else 0
        calc_cost_sql = int(total_campaign_cost / sql) if sql != 0 else 0
        calc_cost_per_conversion = int(
            total_campaign_cost / converted_leads) if converted_leads != 0 else 0
        calc_hit_rate = int(sql / mql * 100) if mql != 0 else 0
        campaign = mongo.db.campaigns.find_one({"_id": ObjectId(campaign_id)})
        calculation = {
            "owning_account": session["user"],
            "account_id": account["_id"],
            "campaign_name": request.form.get("campaign_name"),
            "company_industry": campaign["company_industry"],
            "marketing_qualified_leads": request.form.get(
                "marketing_qualified_leads"),
            "sales_qualified_leads": request.form.get(
                "sales_qualified_leads"),
            "cost_per_marketing_lead": calc_cost_mql,
            "cost_per_sales_lead": calc_cost_sql,
            "cost_per_converted_lead": calc_cost_per_conversion,
            "hit_rate": calc_hit_rate
        }

        mongo.db.calculations.update({"_id": ObjectId(
            calculation_id)}, calculation)
        return redirect(url_for("get_account_profile"))

    calculation = mongo.db.calculations.find_one({"_id": ObjectId(
        calculation_id)})
    campaign = mongo.db.campaigns.find_one({"_id": ObjectId(campaign_id)})

    return redirect(url_for("get_account_profile",
                            campaign=campaign,
                            calculation=calculation))


# Administration


@app.route("/admin")
def admin():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("admin.html", categories=categories)


@app.route("/create_category", methods=["GET", "POST"])
def create_category():
    if request.method == "POST":
        category = {
            "category_type": request.form.get("category_type"),
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.insert_one(category)
        flash("Category succesfully added")
        return redirect(url_for("admin"))

    options = mongo.db.options.find().sort("category_type", 1)
    return render_template("create_category.html", options=options)


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name"),
            "category_type": request.form.get("category_type")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Category successfully updated")
        return redirect(url_for("admin"))

    options = mongo.db.options.find().sort("category_type", 1)
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template(
        "edit_category.html", category=category, options=options)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Category deleted")
    return redirect(url_for("admin"))


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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
