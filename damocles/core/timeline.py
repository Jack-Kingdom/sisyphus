import time
from .item import Item
from .wait import wait
from .utils import SingletonDecorator


@SingletonDecorator
class TimeLine(object):
    def __init__(self):
        self._lst = []

    def push(self, item):
        """
        push an item into time line
        :param item: instance of Item class
        :return: None
        """
        if not isinstance(item, Item):
            raise TypeError('item must be a instance of Item class')

        self._lst.append(item)

        # shift up new item
        child = len(self._lst) - 1
        parent = (child - 1) // 2
        while True:
            if child and self._lst[child] < self._lst[parent]:
                self._lst[child], self._lst[parent] = self._lst[parent], self._lst[child]
                child = parent
                parent = (child - 1) // 2
            else:
                break

    def pop(self):
        """
        pop first item
        :return: Item object
        """

        tail = len(self._lst) - 1
        if tail < 0:
            raise ValueError('no job exist.')

        self._lst[0], self._lst[tail] = self._lst[tail], self._lst[0]
        tail -= 1  # skip last one

        # shift down
        father = 0
        child = father * 2 + 1
        while child <= tail:
            if child + 1 <= tail and self._lst[child + 1] < self._lst[child]:
                child += 1

            if self._lst[child] < self._lst[father]:
                self._lst[father], self._lst[child] = self._lst[child], self._lst[father]
                father = child
                child = father * 2 + 1
            else:
                break

        return self._lst.pop()

    def wait_next(self):

        if not self._lst:
            raise RuntimeError('no job exist')

        idle_time = self._lst[0].time - time.time()
        wait(idle_time if idle_time > 0 else 0)

    def run(self):

        item = self.pop()
        func = item.func

        try:
            item.time = next(item.sequence)
        except StopIteration as e:
            item.time = None
        else:
            self.push(item)

        return func()
