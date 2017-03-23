#coding=utf-8

import gc

from multiprocessing.util import debug
from multiprocessing.pool import MaybeEncodingError

from .data_exchange.operator import DataAcquire

def myworker(inqueue, outqueue, initializer, initargs, maxtasks, reqdataqueue, acqdataqueue):
    assert maxtasks is None or (type(maxtasks) == int and maxtasks > 0)
    put = outqueue.put
    get = inqueue.get

    date_acq = reqdataqueue.put
    data_rev = acqdataqueue.get

    if hasattr(inqueue, '_writer'):
        inqueue._writer.close()
        outqueue._reader.close()

    if initializer is not None:
        initializer(*initargs)

    completed = 0
    # print 'process ready'
    while maxtasks is None or (maxtasks and completed < maxtasks):
        try:
            task = get()
            # print 'first_get',task
        except (EOFError, IOError):
            debug('worker got EOFError or IOError -- exiting')
            break

        if task is None:
            debug('worker got sentinel -- exiting')
            break

        job, i, func, args, kwds = task
        kwds = {'acquire': DataAcquire(date_acq, data_rev)}
        try:
            result = (True, func(*args, **kwds))
        except Exception, e:
            result = (False, e)
        gc.collect()
        try:
            put((job, i, result))
        except Exception as e:
            wrapped = MaybeEncodingError(e, result[1])
            debug("Possible encoding error while sending result: %s" % (
                wrapped))
            put((job, i, (False, wrapped)))
        completed += 1
    # print 'out'
    debug('worker exiting after %d tasks' % completed)