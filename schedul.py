import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)

def print_event(name):
    print 'EVENT:', time.time(), name

print 'START:', time.time()
a = input('')
scheduler.enter(a, 1, print_event, ('first',))
scheduler.enter(10, 1, print_event, ('second',))

scheduler.run()