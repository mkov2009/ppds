from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, Event
from fei.ppds import print


class Shared:
    def __init__(self, count):
        self.n = count
        self.mutex = Mutex()
        self.events = [0] * count
        for j in range(count):
            self.events[j] = Event()
        self.events[0].signal()
        self.array = [0, 1] + [0] * count
        self.sem = [0] * count
        for j in range(count):
            self.sem[j] = Semaphore(0)
        self.sem[0].signal()

    def fibonacci_eve(self, index):
        index += 2
        self.events[index-2].wait()
        self.array[index] = self.array[index - 1] + self.array[index - 2]
        if index-1 != self.n:
            self.events[index-1].signal()

    def fibonacci_sem(self, index):
        index += 2
        self.sem[index-2].wait()
        self.array[index] = self.array[index-1] + self.array[index-2]
        if index - 1 != self.n:
            self.sem[index-1].signal()


def count_fib(s_class, index):
    sleep(randint(1, 10)/10)
    s_class.fibonacci_sem(index)
    # s_class.fibonacci_eve(index)


count_of_threads = 30
s = Shared(count_of_threads)
threads = list()

for i in range(count_of_threads):
    t = Thread(count_fib, s, i)
    threads.append(t)

for t in threads:
    t.join()
print(s.array)

"""Otazky na zamyslenie:
1) Najmenší počet objektov je N, pretože
máme N vlákien a potrebujeme aby sa spúšťali
postupne, takže každé by malo obsahovať
synchornizačný objekt.
2) Ja som použil 2 synchonizačné vzory: udalosti
a signalizáciu. V oboch prípadoch sa používa
N objektov. Pri inicializácii sa signalizuje
udalosť o obidvoch objektoch. Následne pri
iterácií sa použije metóda wait, čím sa
zablokujú vlákna, prebehne výpočet a vlákna
sa opäť odblokujú.
"""
