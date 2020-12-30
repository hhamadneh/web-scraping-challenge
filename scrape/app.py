from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scrape_mars

app = Flask (__name__)
app.config ['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'
mongo = PyMongo (app)

db = mongo.db
collection = db['mars_data']

@app.route("/")
def index():
    try:
        mars_info = list(collection.find())
        return render_template("index.html", mars_info=mars_info)
    except:
        return render_template("empty_scrape.html", mars_info=mars_info)

@app.route("/scrape")
def scrape():
    collection.insert_many(scrape_mars.mars_news())
    collection.insert_many(
            [
                {'featured_img_full':
                scrape_mars.JPL_images()}
            ]
            )
    collection.insert_many(scrape_mars.Mars_Facts())
    collection.insert_many(scrape_mars.Mars_Hemispheres())
    return redirect("/")

@app.route("/clear_data")
def clear_data():
    collection.delete_many({})
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)