from time import time
from multiprocessing import Process
from threading import Thread
import sys
sys.path.append('/Users/macbook/Desktop/projects/cpu-bound/build')
import build.nogil as ng
import multiprocessing as mp
from multiprocessing import Pool


def performance(f):
    def handler(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        resultString = (f'E;apsed time: {(end - start):.3f} with results {result}')
        return resultString
    return handler


@performance
def liner_pi(S):
    result = []

    ng.calc_pi(S, result)
    ng.calc_pi(S, result)
    ng.calc_pi(S, result)
    return result


@performance
def mt_pi(S):
    result = []
    t1 = Thread(target=ng.calc_pi, args=(S, result))
    t2 = Thread(target=ng.calc_pi, args=(S, result))
    t3 = Thread(target=ng.calc_pi, args=(S, result))
    return result


@performance
def mp_pi(S):
    results = mp.Manager().list()

    with Pool(3) as p:
        p.starmap(ng.calc_pi, [(S, results),(S, results),(S, results)])

    return results


@performance
def liner(X):
    result = []
    ng.binary_search(X, result)
    ng.binary_search(X, result)
    ng.binary_search(X, result)
    ng.binary_search(X, result)
    ng.binary_search(X, result)


@performance
def multithreaded(N):
    result = []
    t1 = Thread(target=ng.binary_search, args=(N, result))
    t2 = Thread(target=ng.binary_search, args=(N, result))
    t3 = Thread(target=ng.binary_search, args=(N, result))
    t4 = Thread(target=ng.binary_search, args=(N, result))
    t5 = Thread(target=ng.binary_search, args=(N, result))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    return result


@performance
def multiprocessed(N):
    result = mp.Manager().list()

    p1 = Process(target=ng.binary_search, args=(N, result))
    p2 = Process(target=ng.binary_search, args=(N, result))
    p3 = Process(target=ng.binary_search, args=(N, result))
    p4 = Process(target=ng.binary_search, args=(N, result))
    p5 = Process(target=ng.binary_search, args=(N, result))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()

    return result