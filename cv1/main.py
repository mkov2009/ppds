from fei.ppds import Thread, Mutex


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


class Histogram(dict):
    def __init__(self, seq=[]):
        for item in seq:
            self[item] = self.get(item, 0) + 1


# V tomto pripade je zamok nastaveny na prikaz inkermentacie. Mohlo by sa zdat, ze sa
# cislo nezvysi dvakrat. Ale moze nastat zvysenie pocitadla dvakrat, takze sa dostaneme
# mimo rozsahu listu, alebo sa nezvysi ani raz a teda sa dvakrat inkrementuje na rovnakom
# indexe
def counter_1(shared):
    while True:
        if shared.counter >= shared.end:
            break
        shared.mutex.lock()
        shared.array[shared.counter] += 1
        shared.mutex.unlock()
        shared.counter += 1


# Teraz mame zamok na celom cykle. Takze kazde vlakno bude cakat
# kym sa vykona kompletne telo cyklu. Nemozeme zabudnut na
# odomnknutie pri podmienke, pretoze inak pri prejdeni celeho pola
# by sme sa dostali do deadlocku.
def counter_2(shared):
    while True:
        shared.mutex.lock()
        if shared.counter >= shared.end:
            shared.mutex.unlock()
            break
        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


# V tejto funkcii mame zamok na pocitadle a priradedni pocitadla do
# pomocnej premennej, ta nam zabezpeci, ze kazde vlakno bude pracovat
# ako keby so svojim pocitadlom a nenastane teda zvysenie dvakrat
# alebo ziadne na rovnakom indexe
def counter_3(shared):
    while True:
        shared.mutex.lock()
        tmp = shared.counter
        shared.counter += 1
        shared.mutex.unlock()
        if tmp >= shared.end:
            break
        shared.array[tmp] += 1


for _ in range(10):
    sh = Shared(1_000_000)
    t1 = Thread(counter_3, sh)
    t2 = Thread(counter_3, sh)

    t1.join()
    t2.join()

    print(Histogram(sh.array))
