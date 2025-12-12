import math
import timeit

from integrate import integrate
from concurrent_integrate import integrate_async, integrate_process
from cy_integrate import integrate_cy


def bench_single():
    print("=== Обычная Python integrate ===")
    print(
        timeit.timeit(
            "integrate(math.sin, 0.0, math.pi, n_iter=500_000)",
            globals={"integrate": integrate, "math": math},
            number=3,
        )
    )

    print("=== Cython integrate_cy ===")
    print(
        timeit.timeit(
            "integrate_cy(math.sin, 0.0, math.pi, n_iter=500_000)",
            globals={"integrate_cy": integrate_cy, "math": math},
            number=3,
        )
    )


def bench_concurrent():
    print("=== Потоки + Python integrate ===")
    print(
        timeit.timeit(
            "integrate_async(math.sin, 0.0, math.pi, n_jobs=4, n_iter=500_000)",
            globals={"integrate_async": integrate_async, "math": math},
            number=3,
        )
    )

    print("=== Процессы + Python integrate ===")
    print(
        timeit.timeit(
            "integrate_process(math.sin, 0.0, math.pi, n_jobs=4, n_iter=500_000)",
            globals={"integrate_process": integrate_process, "math": math},
            number=3,
        )
    )


if __name__ == "__main__":
    bench_single()
    bench_concurrent()