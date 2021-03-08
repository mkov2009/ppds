from fei.ppds import Mutex, Semaphore, Thread
from time import sleep
from random import randint


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


def reader(thread_id, shared):
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

for i in range(1):
    t = Thread(writer, f"writer {i}", shared)
    threads.append(t)

for i in range(1):
    t = Thread(reader, f"reader {i}", shared)
    threads.append(t)

for t in threads:
    t.join()
