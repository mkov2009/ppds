class Coroutine(object):
    def __init__(self, target):
        self.target = target

    def run(self):
        return self.target.send(None)

    def get_target(self):
        return self.target


class Scheduler(object):
    def __init__(self):
        self.list = []

    def add_task(self, target):
        task = Coroutine(target)
        self.list.append(task)

    def run(self):
        while len(self.list) != 0:
            task = self.list.pop(0)
            task.run()
            self.add_task(task.get_target())


def test1():
    while True:
        print("Test1")
        yield


def test2():
    while True:
        print("Test2")
        yield


s = Scheduler()
s.add_task(test1())
s.add_task(test2())

s.run()
