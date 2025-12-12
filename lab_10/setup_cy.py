from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
    Extension("cy_integrate", ["cy_integrate.pyx"]),
    Extension("cy_integrate_nogil", ["cy_integrate_nogil.pyx"]),
]

setup(
    name="cy_integrate_all",
    ext_modules=cythonize(extensions, annotate=True, language_level=3),
)