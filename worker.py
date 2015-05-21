import os

import redis
from rq import Worker, Queue, Connection

LISTEN = ['high', 'default', 'low']
CONN = redis.from_url(os.getenv('REDISTOGO_URL'))


def main():
    with Connection(CONN):
        worker = Worker([Queue(l) for l in LISTEN])
        worker.work()

if __name__ == '__main__':
    main()
