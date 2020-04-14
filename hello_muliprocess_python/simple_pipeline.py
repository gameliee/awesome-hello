import multiprocessing
import cv2
import time
import os

class RollBuffer:
    # a FIFO
    # data should index like [last .. -2 -1 first]
    def __init__(self, size=60):
        self.max_size = size
        self.data = [None] * size
        self.first = -1
        self.last = -1
        self.size = 0
        self.locker = multiprocessing.Lock()
        self.firstTime = True

    def print(self):
        self.locker.acquire()
        txt = "QUEUE: first:{} last:{} size:{}".format(self.first, self.last, self.size)
        print(txt)
        self.locker.release()
        return

    def getSize(self):
        self.locker.acquire()
        ret = self.size
        self.locker.release()
        return ret

    def empty(self):
        self.locker.acquire()
        ret = (self.size == 0)
        self.locker.release()
        return ret

    def at(self, index):
        # index should be 0, -1, -2, ... -(size-1)
        self.locker.acquire()
        if index > 0:
            self.locker.release()
            raise BufferError("index out of range, shoule be 0, -1, .., -(size-1)")
        if -index >= self.size:
            self.locker.release()
            raise BufferError("index out of range, size={}".format(self.size))
        temp_index = (self.first + index) % self.max_size
        try:
            ret = self.data[temp_index]
        except:
            self.locker.release()
            raise BufferError("index out of range")
        self.locker.release()
        return ret

    def enqueue(self, item):
        self.locker.acquire()
        if self.firstTime:
            self.last = 0
            self.firstTime = False
        self.first = (self.first + 1) % self.max_size
        if self.size < self.max_size:
            self.data[self.first] = item
            self.size = self.size + 1
        elif self.size == self.max_size:
            self.last = (self.last + 1) % self.max_size
        print("enqueued", self.last, self.first, self.size)
        self.locker.release() 

    def dequeue(self):
        self.locker.acquire()
        if self.size <= 0:
            raise BufferError("empty buffer")
        ret = self.data[self.last]
        self.last = (self.last + 1) % self.max_size
        self.size = self.size - 1
        self.locker.release()
        print("dequeued", self.last, self.first, self.size)
        return ret      


def read(lock, data, running):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("cannot open cap")
        running.value = False
    id = 0
    while running.value:
        start_time = time.time()
        ret, frame = cap.read()
        if ret != True:
            running.value = False
            break
        id = id + 1
        # data.put({'id':id, 'data':frame})
        data.enqueue({'id':id, 'data':frame})
        spent_time = time.time() - start_time # ns
        sleep_time = (33333 - spent_time)/1000 # ms
        print("read", os.getpid(), id, sleep_time, data.getSize())
        time.sleep(sleep_time/1000) #s
    return

def display(lock, data, running):
    curId = -1
    time.sleep(1)
    while running.value:
        start_time = time.time()
        if data.empty():
            time.sleep(1/1000)
            continue
        # lastdata = data.get()
        try:
            # lastdata = data.at(-2)
            lastdata = data.dequeue()
        except Exception as e:
            print("error here", e)
            time.sleep(1/1000)
            continue
        if lastdata['id'] == curId:
            print("not new")
            time.sleep(1/1000)
            continue
        curId = lastdata['id']
        frame = lastdata['data']
        cv2.imshow("capture", frame)
        if 27 == cv2.waitKey(3):
            running.value = False
            break


        spent_time = time.time() - start_time
        sleep_time = (33333 - spent_time)/1000 # ms
        print("disp", os.getpid(), curId, sleep_time, data.getSize())
        time.sleep(sleep_time/1000) #s
    return

def convert(lock, data_src, data_sink, running):
    curId = -1
    time.sleep(1)
    while running.value:
        start_time = time.time()
        if data_src.empty():
            time.sleep(1/1000)
            continue
        # lastdata = data.get()
        try:
            # lastdata = data.at(-2)
            lastdata = data_src.dequeue()
        except Exception as e:
            print("error here", e)
            time.sleep(1/1000)
            continue
        if lastdata['id'] == curId:
            print("not new")
            time.sleep(1/1000)
            continue
        curId = lastdata['id']
        frame = lastdata['data']

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        data_sink.enqueue({'id':curId, 'data':gray})

        spent_time = time.time() - start_time
        sleep_time = (33333 - spent_time)/1000 # ms
        print("convert", os.getpid(), curId, sleep_time, data_src.getSize())
        time.sleep(sleep_time/1000) #s
    return



from multiprocessing.managers import BaseManager
import sys
if __name__ == "__main__":
    # q = multiprocessing.Queue()
    BaseManager.register('RollBuffer', RollBuffer)
    manager = BaseManager()
    manager.start()
    q = manager.RollBuffer()
    qq = manager.RollBuffer()

    # q = RollBuffer()
    running = multiprocessing.Value('b', True)
    running.value = True
    p1 = multiprocessing.Process(target=read, args=(1, q, running))
    p2 = multiprocessing.Process(target=convert, args=(1, q, qq, running))
    p3 = multiprocessing.Process(target=display, args=(1, qq, running))
    p1.start()
    p2.start()
    p3.start()

    time.sleep(60)
    p1.terminate()
    print("terminated p1")
    p2.terminate()
    print("terminated p2")
    p3.terminate()
    print("terminated p3")

    time.sleep(5)
    running.value = False

    p1.join()
    p2.join()





