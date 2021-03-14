from fei.ppds import Mutex, Semaphore, print, Event, Thread
from time import sleep
from random import randint


class LightSwitch(object):
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore):
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class PowerPlant:
    def __init__(self):
        self.monitor_ls = LightSwitch()
        self.no_sensors = Semaphore(1)

    def monitor(self, monitor_id):
        while True:
            self.no_monitors.wait()

            number_of_monitors_reading = self.monitor_ls.lock(self.no_sensors)
            self.no_monitors.signal()
            duration = randint(40, 50) / 1000
            print('monit "%02d": '
                  'pocet_citajucich_monitorov=%02d, '
                  'trvanie_citania=%03f\n' %
                  (monitor_id, number_of_monitors_reading, duration*1000))
            sleep(duration)
            self.monitor_ls.unlock(self.no_sensors)
