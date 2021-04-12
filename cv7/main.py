class Coroutine(object):
    def __init__(self, target, priority):
        self.target = target
        self.priority = priority

    def run(self):
        return self.target.send(None)

    def get_target(self):
        return self.target

    def get_priority(self):
        return self.priority


class Scheduler(object):
    def __init__(self):
        self.list = []

    def add_task(self, target, priority):
        task = Coroutine(target, priority)
        self.list.append(task)

    def run(self):
        self.list.sort(key=sort_func)
        while len(self.list) != 0:
            task = self.list.pop(0)
            task.run()
            self.add_task(task.get_target(), task.get_priority())


def sort_func(task):
    return task.get_priority()


def test1():
    while True:
        print("Test1")
        yield


def test2():
    while True:
        print("Test2")
        yield


s = Scheduler()
s.add_task(test1(), 1)
s.add_task(test2(), 2)

s.run()
