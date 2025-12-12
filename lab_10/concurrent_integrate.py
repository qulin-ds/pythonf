import math
from functools import partial
import concurrent.futures as ftres

from integrate import integrate


def integrate_async(
    f,          # функция одной переменной
    a: float,
    b: float,
    *,
    n_jobs: int = 2,
    n_iter: int = 1000,
) -> float:
    """
    Параллельное численное интегрирование с помощью пула потоков.

    Разбивает отрезок [a, b] на n_jobs подотрезков, на каждом из которых
    вызывается функция integrate(). Результаты суммируются.
    """
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)

    local_n_iter = n_iter // n_jobs
    spawn = partial(
        executor.submit,
        integrate,
        f,
        n_iter=local_n_iter,
    )

    step = (b - a) / n_jobs
    futures = []

    for i in range(n_jobs):
        left = a + i * step
        right = a + (i + 1) * step
        print(f"Работник {i}, границы: {left}, {right}")
        futures.append(spawn(left, right))

    total = 0.0
    for fut in ftres.as_completed(futures):
        total += fut.result()

    executor.shutdown(wait=True)
    return total


def integrate_process(
    f,
    a: float,
    b: float,
    *,
    n_jobs: int = 2,
    n_iter: int = 1000,
) -> float:
    """
    Параллельное численное интегрирование с помощью пула процессов.
    """
    local_n_iter = n_iter // n_jobs
    step = (b - a) / n_jobs

    tasks = [
        (a + i * step, a + (i + 1) * step)
        for i in range(n_jobs)
    ]

    with ftres.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = [
            executor.submit(integrate, f, left, right, n_iter=local_n_iter)
            for (left, right) in tasks
        ]
        total = 0.0
        for fut in ftres.as_completed(futures):
            total += fut.result()
    return total


if __name__ == "__main__":
    print("Threads:", integrate_async(math.sin, 0.0, math.pi, n_jobs=4, n_iter=100_000))
    print("Procs:  ", integrate_process(math.sin, 0.0, math.pi, n_jobs=4, n_iter=100_000))