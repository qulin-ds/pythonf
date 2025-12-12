# cy_integrate.pyx

# cython: language_level=3

# cy_integrate_nogil.pyx
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True

cdef double _integrate_raw_nogil(double a, double b, long n_iter) nogil:
    cdef long i
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        # пример: f(x) = x^2
        acc += x * x * step
    return acc


сdef integrate_nogil(double a, double b, long n_iter=100000):
    """
    Python-обёртка над noGIL-функцией _integrate_raw_nogil.
    """
    return _integrate_raw_nogil(a, b, n_iter)