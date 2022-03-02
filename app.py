# Use flask to render a template, redirecting to another URL and creating an URL
from flask import Flask, render_template, redirect, url_for
# Use PyMongo to interact with our Mongo Database
from flask_pymongo import PyMongo
# To use the scraping code, we will convert from Jupyter Notebook to Python
import scraping

# Set up the Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection. 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the HTML page.
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Add next route, the scraping.
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code=302)

# Run it
if __name__ == "__main__":
    app.run()



