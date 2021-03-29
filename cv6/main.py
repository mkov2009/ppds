from fei.ppds import Mutex, Semaphore, print, Thread, Event
from time import sleep
from random import randint


class Barrier:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        self.mutex.lock()
        self.count += 1
        if self.count == self.n:
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()


class Shared(object):
    def __init__(self):
        self.mutex = Semaphore(1)
        self.oxygenCount = 0
        self.hydrogenCount = 0
        self.oxyQueue = Semaphore(1)
        self.hydroQueue = Semaphore(2)
        self.barrier = Barrier(3)

    def oxygen(self):
        sleep(randint(1, 10) / 10)
        self.mutex.wait()
        self.oxygenCount += 1
        print("Oxygen count = ", self.oxygenCount)
        if self.hydrogenCount < 2:
            self.mutex.signal()
        else:
            self.oxygenCount -= 1
            self.hydrogenCount -= 2
            self.oxyQueue.signal()
            self.hydroQueue.signal(2)
            print("bonding")
            print("count after bond: oxygen: %d, hydrogen: %d\n" % (self.oxygenCount, self.hydrogenCount))

        self.oxyQueue.wait()
        self.barrier.wait()
        self.mutex.signal()

    def hydrogen(self):
        sleep(randint(1, 10) / 10)
        self.mutex.wait()
        self.hydrogenCount += 1
        print("Hydrogen count = ", self.hydrogenCount)
        if self.hydrogenCount < 2 or self.oxygenCount < 1:
            self.mutex.signal()
        else:
            self.oxygenCount -= 1
            self.hydrogenCount -= 2
            self.oxyQueue.signal()
            self.hydroQueue.signal(2)
            print("bonding")
            print("count after bond: oxygen: %d, hydrogen: %d\n" % (self.oxygenCount, self.hydrogenCount))

        self.hydroQueue.wait()
        self.barrier.wait()


threads = []
sh = Shared()
for i in range(100):
    t = Thread(sh.oxygen)
    threads.append(t)

for i in range(200):
    t = Thread(sh.hydrogen)
    threads.append(t)

for t in threads:
    t.join()
