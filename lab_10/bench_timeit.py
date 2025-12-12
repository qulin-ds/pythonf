import math
import timeit

from integrate import integrate


def main() -> None:
    for n_iter in (10_000, 50_000, 100_000, 500_000):
        t = timeit.timeit(
            "integrate(math.sin, 0.0, math.pi, n_iter=n_iter)",
            globals={"integrate": integrate, "math": math, "n_iter": n_iter},
            number=5,  # 5 повторов для усреднения
        )
        print(f"n_iter={n_iter:>7}: {t:.4f} сек (5 запусков)")

    # здесь же можно записать результаты в файл/таблицу руками для отчёта


if __name__ == "__main__":
    main()