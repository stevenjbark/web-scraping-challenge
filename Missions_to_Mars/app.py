from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

#Import scrape_mars.py for scraping web
import scrape_mars

app = Flask(__name__)

#Setup MongoDB connection as in scrape_mars.py. Conn = connection port info, 
#client is connection client.
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_DataDB"
mongo = PyMongo(app)

#Connect to db = Mars_DataDB database and scraped_mars_data is the collection.
scraped_mars_data = mongo.db.scraped_mars_data

#Already set to drop any collection data prior to appending new data in scrape_mars.py.
#scraped_mars_data.drop()

#Route to render the index.html page with data from the Mars_DataDB
@app.route("/")
def index():
    mars_data = scraped_mars_data.find()
    mars_data2 = scraped_mars_data.find()
    return render_template("index.html", mars_data=mars_data, mars_data2=mars_data2)

#Route to scrape mars data using the scrape_mars.py program, then redirect to index.html data page.
@app.route("/scrape")
def scrape():

    #Scrape using scrape_mars.scrape() function from scrape_mars.py. Unlike class example,
    #the scraped data is already inserted into MongoDB, so no insert_many required.
    scrape_mars.scrape()

    #Redirect function to send us back to main html page.
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)