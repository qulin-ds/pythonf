"""Лабораторная работа: Численные вычисления и анализ данных с NumPy.

Модуль содержит функции для работы с массивами, матрицами,
статистического анализа и визуализации данных.
"""

import os
from typing import Dict, Union

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")


# ============================================================
# 1. СОЗДАНИЕ И ОБРАБОТКА МАССИВОВ
# ============================================================


def create_vector() -> np.ndarray:
    """Создать одномерный массив целых чисел от 0 до 9.

    Returns:
        np.ndarray: Массив формы (10,) с элементами [0, 1, ..., 9].
    """
    return np.arange(10)


def create_matrix() -> np.ndarray:
    """Создать матрицу 5x5 со случайными числами из [0, 1).

    Returns:
        np.ndarray: Матрица формы (5, 5) со значениями в диапазоне [0, 1).
    """
    return np.random.rand(5, 5)


def reshape_vector(vec: np.ndarray) -> np.ndarray:
    """Преобразовать одномерный массив формы (10,) в матрицу (2, 5).

    Args:
        vec: Входной массив формы (10,).

    Returns:
        np.ndarray: Массив формы (2, 5).
    """
    return vec.reshape(2, 5)


def transpose_matrix(mat: np.ndarray) -> np.ndarray:
    """Транспонировать матрицу.

    Args:
        mat: Входная двумерная матрица.

    Returns:
        np.ndarray: Транспонированная матрица.
    """
    return mat.T


# ============================================================
# 2. ВЕКТОРНЫЕ ОПЕРАЦИИ
# ============================================================


def vector_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Выполнить поэлементное сложение двух векторов.

    Args:
        a: Первый вектор.
        b: Второй вектор той же длины.

    Returns:
        np.ndarray: Результат поэлементного сложения.
    """
    return a + b


def scalar_multiply(vec: np.ndarray, scalar: Union[int, float]) -> np.ndarray:
    """Умножить вектор на скаляр.

    Args:
        vec: Входной вектор.
        scalar: Число-множитель.

    Returns:
        np.ndarray: Результат умножения каждого элемента на скаляр.
    """
    return vec * scalar


def elementwise_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Выполнить поэлементное умножение двух массивов.

    Args:
        a: Первый массив.
        b: Второй массив той же формы.

    Returns:
        np.ndarray: Результат поэлементного умножения.
    """
    return a * b


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """Вычислить скалярное произведение двух векторов.

    Args:
        a: Первый вектор.
        b: Второй вектор той же длины.

    Returns:
        float: Скалярное произведение.
    """
    return np.dot(a, b)


# ============================================================
# 3. МАТРИЧНЫЕ ОПЕРАЦИИ
# ============================================================


def matrix_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Выполнить матричное умножение двух матриц.

    Args:
        a: Первая матрица формы (m, n).
        b: Вторая матрица формы (n, k).

    Returns:
        np.ndarray: Результат матричного умножения формы (m, k).
    """
    return a @ b


def matrix_determinant(a: np.ndarray) -> float:
    """Вычислить определитель квадратной матрицы.

    Args:
        a: Квадратная матрица.

    Returns:
        float: Определитель матрицы.
    """
    return np.linalg.det(a)


def matrix_inverse(a: np.ndarray) -> np.ndarray:
    """Вычислить обратную матрицу.

    Args:
        a: Невырожденная квадратная матрица.

    Returns:
        np.ndarray: Обратная матрица.
    """
    return np.linalg.inv(a)


def solve_linear_system(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Решить систему линейных уравнений Ax = b.

    Args:
        a: Матрица коэффициентов A.
        b: Вектор свободных членов b.

    Returns:
        np.ndarray: Вектор решения x.
    """
    return np.linalg.solve(a, b)


# ============================================================
# 4. СТАТИСТИЧЕСКИЙ АНАЛИЗ
# ============================================================


def load_dataset(path: str = "data/students_scores.csv") -> np.ndarray:
    """Загрузить CSV-файл и вернуть данные как NumPy-массив.

    Args:
        path: Путь к CSV-файлу.

    Returns:
        np.ndarray: Числовые данные из файла.
    """
    return pd.read_csv(path).to_numpy()


def statistical_analysis(data: np.ndarray) -> Dict[str, float]:
    """Вычислить основные статистические показатели массива.

    Рассчитывает среднее, медиану, стандартное отклонение,
    минимум, максимум, 25-й и 75-й перцентили.

    Args:
        data: Одномерный массив числовых данных.

    Returns:
        dict: Словарь с ключами ``mean``, ``median``, ``std``,
              ``min``, ``max``, ``percentile_25``, ``percentile_75``.
    """
    return {
        "mean": np.mean(data),
        "median": np.median(data),
        "std": np.std(data),
        "min": np.min(data),
        "max": np.max(data),
        "percentile_25": np.percentile(data, 25),
        "percentile_75": np.percentile(data, 75),
    }


def normalize_data(data: np.ndarray) -> np.ndarray:
    """Выполнить Min-Max нормализацию массива в диапазон [0, 1].

    Формула: (x - min) / (max - min).

    Args:
        data: Входной массив числовых данных.

    Returns:
        np.ndarray: Нормализованный массив.
    """
    data_min = np.min(data)
    data_max = np.max(data)
    return (data - data_min) / (data_max - data_min)


# ============================================================
# 5. ВИЗУАЛИЗАЦИЯ
# ============================================================


def plot_histogram(data: np.ndarray) -> None:
    """Построить и сохранить гистограмму распределения оценок.

    Args:
        data: Одномерный массив оценок.
    """
    os.makedirs("plots", exist_ok=True)
    plt.figure()
    plt.hist(data, bins=10, edgecolor="black", alpha=0.7)
    plt.title("Распределение оценок по математике")
    plt.xlabel("Оценка")
    plt.ylabel("Частота")
    plt.savefig("plots/histogram.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_heatmap(matrix: np.ndarray) -> None:
    """Построить и сохранить тепловую карту корреляции.

    Args:
        matrix: Матрица корреляции.
    """
    os.makedirs("plots", exist_ok=True)
    plt.figure()
    sns.heatmap(matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Корреляционная матрица предметов")
    plt.savefig("plots/heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_line(x: np.ndarray, y: np.ndarray) -> None:
    """Построить и сохранить линейный график оценок студентов.

    Args:
        x: Номера студентов.
        y: Оценки студентов.
    """
    os.makedirs("plots", exist_ok=True)
    plt.figure()
    plt.plot(x, y, marker="o", linestyle="-", color="steelblue")
    plt.title("Оценки студентов по математике")
    plt.xlabel("Номер студента")
    plt.ylabel("Оценка")
    plt.grid(True, alpha=0.3)
    plt.savefig("plots/line_plot.png", dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    print(
        "Запустите python -m pytest test.py -v "
        "для проверки лабораторной работы."
    )
