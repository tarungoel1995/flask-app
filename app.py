from rediscluster import RedisCluster
import time
from flask import Flask
import os
from gevent.pywsgi import WSGIServer


app = Flask(__name__)
#startup_nodes = [{"host": "redis-cluster", "port": "6379"}]
startup_nodes = [{"host": os.environ.get('REDIS_HOST', 'redis'), "port": "6379"}]
cache = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)


def get_hit_count():
    return cache.incr('hits')


@app.route('/')
def hit():
    count = get_hit_count()
    return 'I have been hit %i times since deployment.\n' % int(count)


if __name__ == "__main__":
#    app.run(host="0.0.0.0", debug=True)
     http_server = WSGIServer(('', 5000), app)
     http_server.serve_forever()
