from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import CONN
from tasks import pin

SCHED = BlockingScheduler()
QUEUE = Queue(connection=CONN)


@SCHED.scheduled_job('cron', day_of_week='sun', timezone='UTC')
def weekly_pin():
    QUEUE.enqueue(pin)

if __name__ == '__main__':
    SCHED.start()
