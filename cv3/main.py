from fei.ppds import Mutex, Semaphore, Thread
from time import sleep
from random import randint

"""Odpovede na otazky:
    5) Vyhladovanie mi nastavalo pri nastaveni:
    priemerny cas 0.5, pocet zapisovatelov 1 a
    pocet citatelov 3. Pridanie turniketu
    problem vyriesilo.

    7) Vyhladovanie citatelov mi nenastalo ani
    pri nastaveni s rovnakym priemernym casom,
    poctom citatelov 1 a poctom zapisovatelov
    200. Z tohto usudzujem, ze nenastava tento
    pripad. Zvacsa byva citatelov o viac ako
    zapisovatelov.
"""


class LightSwitch(object):
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class Shared():
    def __init__(self):
        self.room = Semaphore(1)
        self.turn = Semaphore(1)


def writer(shared):
    while True:
        sleep(randint(0, 10) / 10)

        shared.turn.wait()
        shared.room.wait()
        print("W - inside ")
        sleep(0.3 + randint(0, 4) / 10)
        shared.room.signal()
        shared.turn.signal()
        print("W - after ")


def reader(shared):
    while True:
        shared.turn.wait()
        shared.turn.signal()
        sleep(randint(0, 10) / 10)

        lightSwitch.lock(shared.room)
        print("R - inside ")
        sleep(0.3 + randint(0, 4) / 10)
        lightSwitch.unlock(shared.room)
        print("R - after ")


shared = Shared()
lightSwitch = LightSwitch()
threads = []

# Pocet zapisovatelov
n_of_writers = 1

# Pocet citatelov
n_of_readers = 3

for i in range(n_of_writers):
    t = Thread(writer, shared)
    threads.append(t)

for i in range(n_of_readers):
    t = Thread(reader, shared)
    threads.append(t)

for t in threads:
    t.join()
