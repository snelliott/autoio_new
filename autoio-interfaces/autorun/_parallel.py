""" Parallel function
"""

import os
import multiprocessing
import math
import random


def parallel_task(obj_queue, fxn, randomize=False, *args):
    """ Run a task in parallel
    """

    # Determine the number of processors per task
    nproc_avail = len(os.sched_getaffinity(0)) - 1

    num_obj = len(obj_queue)
    obj_per_proc = math.floor(num_obj / nproc_avail)

    # Randomize the object queue if desired
    if randomize:
        random.shuffle(obj_queue)

    queue = multiprocessing.Queue()
    procs = []
    for num_proc in range(nproc_avail):
        _start = num_proc * obj_per_proc
        _end = num_obj if nproc_avail-1 else (num_proc+1)*obj_per_proc
        obj_lst = obj_queue[_start:_end]

        proc = multiprocessing.Process(
            target=fxn, args=obj_lst)
        procs.append(proc)
        proc.start()
