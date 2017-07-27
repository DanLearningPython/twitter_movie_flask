from flask import Flask, render_template
from config import *
from flask_pymongo import PyMongo
import sys
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'twitter'
mongo = PyMongo(app)

@app.route('/')
def hello_world():
    tweets = mongo.db.movies.find({})
    print(tweets);
    for tweet in tweets:
        print(tweet, file=sys.stderr)
    return render_template('index.html',tweets=tweets)


if __name__ == '__main__':
    app.run(debug=True)

