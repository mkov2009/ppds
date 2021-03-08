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


def writer(thread_id, shared):
    # pred kazdym pokusom o zapis pocka v intervale <0.0; 1> sekundy
    sleep(randint(0, 10) / 10)

    shared.room.wait()
    print(thread_id)
    # simulujeme dlzku zapisu v intervale <0.3; 0.7> sekundy
    sleep(0.3 + randint(0, 4) / 10)
    shared.room.signal()


def reader(thread_id, shared):
    lightSwitch.lock(shared.room)
    sleep(0.3 + randint(0, 4) / 10)
    print(thread_id)
    lightSwitch.unlock(shared.room)


shared = Shared()
lightSwitch = LightSwitch()
threads = []

for i in range(10):
    t = Thread(writer, f"writer {i}", shared)
    threads.append(t)

    t = Thread(reader, f"reader {i}", shared)
    threads.append(t)


for t in threads:
    t.join()
