from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_costa
import os

if os.environ.get('MONGODB_URI'):
    mongo_uri = os.environ.get('MONGODB_URI')
    flask_debug = False
else:
    from dev_config import mongo_uri, flask_debug

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri=mongo_uri)
destination_data = []

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination = mongo.db.destination_data.find_one()
    

    # Return template and data
    return render_template("index.html", vacation=destination)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    results = scrape_costa.scrape_info()

    # Update the Mongo database using update and upsert=True
    destination_data = mongo.db.destination_data
    page_data = results
    destination_data.update({}, page_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=flask_debug)
