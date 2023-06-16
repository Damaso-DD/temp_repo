# app.py
import json

from celery import Celery
from flask import Flask, g, request
from flask_cors import CORS
from redis import Redis

app = Flask(__name__)
CORS(app)


celery = Celery()
celery.conf.broker_url = 'redis://redis:6379/0'


def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route('/food', methods=['GET', 'POST'])
def suggestions():
    if request.method == 'POST':
        food_suggestion = request.json["food"]
        celery.send_task('tasks.update_database', (food_suggestion,))
        return app.response_class(
            status=200,
            mimetype='application/json'
        )
    elif request.method == 'GET':
        redis = get_redis()
        food_suggestions = []
        if redis.llen("suggestions") > 0:
            answer = redis.lrange('suggestions', 0, -1)[0]
            food_suggestions = json.loads(answer)
            food_suggestions = list(map(lambda x: {'name': x[0]}, food_suggestions))
        return app.response_class(
            response=json.dumps({'suggestions': food_suggestions}),
            status=200,
            mimetype='application/json'
        )



@app.route("/health", methods=['GET'])
def health():
    return app.response_class(
        status=200,
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)