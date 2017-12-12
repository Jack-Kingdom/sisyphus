import time
from sisyphus.core import Job, TimeLine

now = time.time()
before = [now for _ in range(10)]


def func1(num):
    print(num, time.time() - before[num])
    before[num] = time.time()


if __name__ == '__main__':
    tl = TimeLine()
    tl.add(Job(iter([now + i for i in [2, 3, 5]]), func1, 3))
    while tl.has_jobs():
        tl.wait_next()
        tl.run()
    else:
        print("all job run over")
