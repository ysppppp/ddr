from threading import Thread, Lock
import time

class Counter(object):
    def __init__(self):
        self.value = 0
    def increment(self):
        self.value += 1
    def decrement(self):
        self.value -= 1

c = Counter()
l = Lock()

def go_up(times):
    with l:
        for i in range(times):
            c.increment()
            print(c.value)
            time.sleep(1)

def go_down(times):
    with l:
        for i in range(times):
            c.decrement()
            print(c.value)
            time.sleep(1)

t1 = Thread(target=go_up, args=[1000])
t1.start()
t2 = Thread(target=go_down, args=[1000])
t2.start()
t1.join()
t2.join()


# from threading import Thread, Event
# from queue import Queue
# # if Python 2: instead, use
# # from Queue import Queue
# import time
#
# class Counter(object):
#     def __init__(self):
#         self.value = 0
#     def increment(self):
#         self.value += 1
#     def decrement(self):
#         self.value -= 1
#
# e = Event()
# q = Queue()
#
# def go_up(times):
#     c = Counter()
#     for i in range(times):
#         c.increment()
#         time.sleep(0.1)
#         print(c.value)
#         q.put(c.value)
#
# def check_value(threshold):
#     while True:
#         if q.get() > threshold:
#             e.set()
#             break
#
# def alarm():
#     e.wait()
#     print("WARNING: high value!")
#
# def reset_alarm():
#     print("hi")
#     e.clear()
#
#
# t1 = Thread(target=go_up, args=[100])
# t1.start()
# t2 = Thread(target=check_value, args=[50])
# t2.start()
# t3 = Thread(target=alarm)
# t3.start()
# t1.join()
# t2.join()
# t3.join()
#
# from threading import Thread
# import time
#
# class Counter(object):
#     def __init__(self):
#         self.value = 0
#     def increment(self):
#         self.value += 1
#     def decrement(self):
#         self.value -= 1
#
# c = Counter()
#
# def go_up(times):
#     # for i in range(times):
#     while True:
#         c.increment()
#         time.sleep(1)
#         print('hi')
#
# def go_down(times):
#     # for i in range(times):
#     while True:
#         c.decrement()
#         time.sleep(2)
#         print('bye')
#
# t1 = Thread(target=go_up, args=[1000])
# t1.start()
# t2 = Thread(target=go_down, args=[1000])
# t2.start()
# t1.join()
# t2.join()
