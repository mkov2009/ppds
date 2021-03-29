from fei.ppds import Mutex, Semaphore, print, Thread, Event
from time import sleep
from random import randint


"""Zadanie Tvorba molekul vody"""


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
        """sleep na simulovanie náhodného príchodu atómov"""
        sleep(randint(1, 10) / 10)
        """
            spoločný semafor, na ktorom atómy čakajú
            a vstupujú po jednom a zvýšenie počídla, keďže vstupujú
            po jednom, tak nepotrebujeme už nijak chrániť prístup k
            premennej oxygenCount.
        """
        self.mutex.wait()
        self.oxygenCount += 1
        print("Oxygen count = ", self.oxygenCount)
        """
            podmienka, ktora overuje, či je aj dostatok atómov
            na tvorbu molekuly vody, ak nie je, tak pusti ďalší
            atóm cez semafor, inak spraví zlúčenie.
        """
        if self.hydrogenCount < 2:
            self.mutex.signal()
        else:
            self.oxygenCount -= 1
            self.hydrogenCount -= 2
            self.oxyQueue.signal()
            self.hydroQueue.signal(2)
            print("bonding")
            print("count after bond: oxygen: %d, hydrogen: %d\n" %
                  (self.oxygenCount, self.hydrogenCount))

        """
            Kyslík čaká, kým mu prídu dva vodíky, cez prejde
            len jeden.
        """
        self.oxyQueue.wait()
        """
            Bariera, ktorá pusti cez 3 prvky, aby nenastalo, že nejaký
            prvok sa stihne obehnúť
        """
        self.barrier.wait()
        """
            Po úšpešnom spojení nastane, kyslík otvorí semafor pre
            ďalší prvok aby nenastal deadlock.
        """
        self.mutex.signal()

    def hydrogen(self):
        """sleep na simulovanie náhodného príchodu atómov"""
        sleep(randint(1, 10) / 10)
        """
            spoločný semafor, na ktorom atómy čakajú
            a vstupujú po jednom a zvýšenie počídla, keďže vstupujú
            po jednom, tak nepotrebujeme už nijak chrániť prístup k
            premennej hydrogenCount.
        """
        self.mutex.wait()
        self.hydrogenCount += 1
        print("Hydrogen count = ", self.hydrogenCount)
        """
            podmienka, ktora overuje, či je aj dostatok atómov
            na tvorbu molekuly vody a kyslíka, ak nie je, tak pustí
            ďalší atóm cez semafor, inak spraví zlúčenie.
        """
        if self.hydrogenCount < 2 or self.oxygenCount < 1:
            self.mutex.signal()
        else:
            self.oxygenCount -= 1
            self.hydrogenCount -= 2
            self.oxyQueue.signal()
            self.hydroQueue.signal(2)
            print("bonding")
            print("count after bond: oxygen: %d, hydrogen: %d\n" %
                  (self.oxygenCount, self.hydrogenCount))

        """
            Vodík čaká, kým mu príde ďalší vodík a kyslík,
            cez prejdu dva.
        """
        self.hydroQueue.wait()
        """
            Bariera, ktorá pusti cez 3 prvky, aby nenastalo, že nejaký
            prvok sa stihne obehnúť.
        """
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
