from flask import Flask, Response, request
import sys
import json
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'twitter'
mongo = PyMongo(app)


@app.after_request
def after_request(response):
    #CORS support
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/', methods=['GET','POST', 'OPTIONS'])
def get_tweets():

    mongo_filter = {}

    if 'after' in request.args:
        after_timestamp = request.args.get("after")
        after_timestamp = get_int(after_timestamp)
        if after_timestamp > 0:
            mongo_filter = {
                'timestamp': {
                    '$gt': after_timestamp
                }
            }

    tweets = mongo.db.movies.find(mongo_filter).sort('timestamp', 1 )

    json_result = to_json(tweets)

    resp = Response(response=json_result,
                    status=200,
                    mimetype="application/json")

    return resp

def get_int(string):
    try:
        num = int(string)
        return num
    except ValueError:
        return None

def to_json(mongo_result):

    json_result = []

    for result in mongo_result:
        tmp = {
            'checksum': result['checksum'],
            'topic': result['topic'],
            'timestamp' : result['timestamp'],
            'tweet': result['tweet'],
            'sentiment': {
                'positive': result['sentiment'][1],
                'negative': result['sentiment'][0]
            }
        }
        json_result.append(tmp.copy())

    return json.dumps(json_result)


if __name__ == '__main__':
    app.run(debug=True)

