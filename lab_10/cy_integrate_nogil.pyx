# cy_integrate_nogil.pyx

# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True
from cython.parallel import prange
import cython

@cython.cfunc
@cython.locals(
    i=cython.long,
    step=cython.double,
    acc=cython.double,
    x=cython.double,
)
def _integrate_raw_nogil(double a, double b, long n_iter) nogil:
    cdef long i
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        # здесь нет вызова Python-функции, нужно чистое C-выражение
        # пример: интеграл от x*x
        acc += x * x * step
    return acc


def integrate_nogil(double a, double b, long n_iter=100000):
    """
    Пример noGIL-версии для конкретной функции f(x) = x^2.
    Для обобщённой f(x) придётся отказаться от чистого nogil.
    """
    return _integrate_raw_nogil(a, b, n_iter)