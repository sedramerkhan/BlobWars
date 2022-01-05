import inspect
import threading
import time

out = {}


def measure(fun):
    start = time.time()
    out[inspect.getsource(fun)] = (fun(), time.time() - start)



def compare(fun1, fun2):
    # creating thread
    global out
    out = {}
    t1 = threading.Thread(target=lambda: measure(fun1))
    t2 = threading.Thread(target=lambda: measure(fun2))
    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Done!")
    return out
