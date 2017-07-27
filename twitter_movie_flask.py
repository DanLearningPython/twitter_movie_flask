from flask import Flask, Response

import json
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'twitter'
mongo = PyMongo(app)


@app.route('/')
def hello_world():
    tweets = mongo.db.movies.find({})

    json_result = to_json(tweets)

    resp = Response(response=json_result,
                    status=200,
                    mimetype="application/json")

    return resp


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

