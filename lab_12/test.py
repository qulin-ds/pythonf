"""Тесты для лабораторной работы по NumPy."""

import os

import numpy as np

from main import (
    create_matrix,
    create_vector,
    dot_product,
    elementwise_multiply,
    load_dataset,
    matrix_determinant,
    matrix_inverse,
    matrix_multiply,
    normalize_data,
    plot_heatmap,
    plot_histogram,
    plot_line,
    reshape_vector,
    scalar_multiply,
    solve_linear_system,
    statistical_analysis,
    vector_add,
)


def test_create_vector() -> None:
    """Проверяет создание вектора от 0 до 9."""
    v = create_vector()
    assert isinstance(v, np.ndarray)
    assert v.shape == (10,)
    assert np.array_equal(v, np.arange(10))


def test_create_matrix() -> None:
    """Проверяет создание матрицы 5x5 со значениями [0, 1)."""
    m = create_matrix()
    assert isinstance(m, np.ndarray)
    assert m.shape == (5, 5)
    assert np.all((m >= 0) & (m < 1))


def test_reshape_vector() -> None:
    """Проверяет преобразование формы (10,) -> (2, 5)."""
    v = np.arange(10)
    reshaped = reshape_vector(v)
    assert reshaped.shape == (2, 5)
    assert reshaped[0, 0] == 0
    assert reshaped[1, 4] == 9


def test_vector_add() -> None:
    """Проверяет поэлементное сложение векторов."""
    assert np.array_equal(
        vector_add(np.array([1, 2, 3]), np.array([4, 5, 6])),
        np.array([5, 7, 9]),
    )
    assert np.array_equal(
        vector_add(np.array([0, 1]), np.array([1, 1])),
        np.array([1, 2]),
    )


def test_scalar_multiply() -> None:
    """Проверяет умножение вектора на скаляр."""
    assert np.array_equal(
        scalar_multiply(np.array([1, 2, 3]), 2),
        np.array([2, 4, 6]),
    )


def test_elementwise_multiply() -> None:
    """Проверяет поэлементное умножение."""
    assert np.array_equal(
        elementwise_multiply(np.array([1, 2, 3]), np.array([4, 5, 6])),
        np.array([4, 10, 18]),
    )


def test_dot_product() -> None:
    """Проверяет скалярное произведение."""
    assert dot_product(np.array([1, 2, 3]), np.array([4, 5, 6])) == 32
    assert dot_product(np.array([2, 0]), np.array([3, 5])) == 6


def test_matrix_multiply() -> None:
    """Проверяет матричное умножение."""
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[2, 0], [1, 2]])
    assert np.array_equal(matrix_multiply(a, b), a @ b)


def test_matrix_determinant() -> None:
    """Проверяет вычисление определителя."""
    a = np.array([[1, 2], [3, 4]])
    assert round(matrix_determinant(a), 5) == -2.0


def test_matrix_inverse() -> None:
    """Проверяет вычисление обратной матрицы."""
    a = np.array([[1, 2], [3, 4]])
    inv_a = matrix_inverse(a)
    assert np.allclose(a @ inv_a, np.eye(2))


def test_solve_linear_system() -> None:
    """Проверяет решение СЛАУ."""
    a = np.array([[2, 1], [1, 3]])
    b = np.array([1, 2])
    x = solve_linear_system(a, b)
    assert np.allclose(a @ x, b)


def test_load_dataset() -> None:
    """Проверяет загрузку CSV в NumPy-массив."""
    test_data = "math,physics,informatics\n78,81,90\n85,89,88"
    with open("test_data.csv", "w") as f:
        f.write(test_data)
    try:
        data = load_dataset("test_data.csv")
        assert data.shape == (2, 3)
        assert np.array_equal(data[0], [78, 81, 90])
    finally:
        os.remove("test_data.csv")


def test_statistical_analysis() -> None:
    """Проверяет статистический анализ."""
    data = np.array([10, 20, 30])
    result = statistical_analysis(data)
    assert result["mean"] == 20
    assert result["min"] == 10
    assert result["max"] == 30


def test_normalization() -> None:
    """Проверяет Min-Max нормализацию."""
    data = np.array([0, 5, 10])
    norm = normalize_data(data)
    assert np.allclose(norm, np.array([0, 0.5, 1]))


def test_plot_histogram() -> None:
    """Проверяет, что гистограмма строится без ошибок."""
    data = np.array([1, 2, 3, 4, 5])
    plot_histogram(data)


def test_plot_heatmap() -> None:
    """Проверяет, что тепловая карта строится без ошибок."""
    matrix = np.array([[1, 0.5], [0.5, 1]])
    plot_heatmap(matrix)


def test_plot_line() -> None:
    """Проверяет, что линейный график строится без ошибок."""
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    plot_line(x, y)
