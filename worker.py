import os
import redis
from rq import Worker, Queue, Connection

LISTEN = ['high', 'default', 'low']
conn = redis.from_url(os.getenv('REDISTOGO_URL'))

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, LISTEN))
        worker.work()
