from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
from tasks import pin

sched = BlockingScheduler()
q = Queue(connection=conn)


@sched.scheduled_job('cron', day_of_week='sun', timezone='UTC')
def weekly_pin():
    q.enqueue(pin)


if __name__ == '__main__':
    sched.start()
