import math
import timeit

from concurrent_integrate import integrate_async, integrate_process


def bench(func_name, func, n_jobs_values, n_iter):
    for n_jobs in n_jobs_values:
        t = timeit.timeit(
            "func(math.sin, 0.0, math.pi, n_jobs=n_jobs, n_iter=n_iter)",
            globals={"func": func, "math": math, "n_jobs": n_jobs, "n_iter": n_iter},
            number=3,
        )
        print(f"{func_name}, n_jobs={n_jobs}: {t:.4f} сек (3 запуска)")


if __name__ == "__main__":
    jobs = (2, 4, 6, 8)
    n_iter = 400_000

    print("=== Потоки ===")
    bench("threads", integrate_async, jobs, n_iter)

    print("\n=== Процессы ===")
    bench("processes", integrate_process, jobs, n_iter)