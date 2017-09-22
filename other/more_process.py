import multiprocessing
import numpy as np
lock = multiprocessing.Lock()
def writer_proc(q):
    try:
        #if lock.acquire():
        print('write')
        q.put(1)
        q.put({'fe':12})
        q.put(np.array([1,2]))
        # lock.release()
    except:
        pass

def reader_proc(q):
    try:

        print('read')
        while True:
            print(q.get())
        # lock.release()
    except:
        pass

if __name__ == "__main__":
    q = multiprocessing.Queue()
    writer = multiprocessing.Process(target=writer_proc, args=(q,))
    reader = multiprocessing.Process(target=reader_proc, args=(q,))
    writer.start()
    reader.start()

    writer.join()
    reader.terminate()