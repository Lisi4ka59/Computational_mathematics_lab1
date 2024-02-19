import tkinter as tk
import sys


def show_answer(answer, matrix, vector, size, accuracy):
    root = tk.Tk()
    root.title("Ответ")
    root.minsize(300, 300)
    format_answer = "Для данной СЛАУ:\n\n"
    j = 0
    for i in range(size):
        for j in range(size - 1):
            if matrix[i][j + 1] < 0:
                plus = " - "
            else:
                plus = " + "
            if j == 0:
                format_answer += (str(int(matrix[i][j]) if matrix[i][j].is_integer() else matrix[i][j]) + "×X" +
                                  str(j + 1) + plus)
            else:
                format_answer += (str(abs(int(matrix[i][j]) if matrix[i][j].is_integer() else matrix[i][j])) + "×X" +
                                  str(j + 1) + plus)
        format_answer += (
                    str(abs(int(matrix[i][j + 1]) if matrix[i][j + 1].is_integer() else matrix[i][j + 1])) + "×X" +
                    str(j + 2))
        format_answer += " = " + str(int(vector[i]) if vector[i].is_integer() else vector[i]) + "\n"
    format_answer += "\n" + "Ответ с точностью до " + str(accuracy) + ":" + "\n"
    format_answer += answer
    label = tk.Label(root, text=format_answer)
    label.pack()
    root.mainloop()


def calculate_matrix(matrix, vector, size, accuracy):
    rnd = 1
    rnd_accuracy = 0
    if '.' in str(accuracy):
        rnd = max(len(str(accuracy)) - str(accuracy).index('.') - 1, 3)
        rnd_accuracy = rnd + 3
    iteration_count = 0

    if calculate_determinant(matrix) == 0:
        show_answer("\nОпределитель матрицы равен 0! ", matrix, vector, size, accuracy)
        return

    diagonal_matrix, diagonal_vector = diagonal_dominance(matrix, size, vector, accuracy)
    if diagonal_matrix is None:
        return

    # теперь у нас есть матрица составленная с диагональным преобладанием
    reduced_matrix = [[0.0 for _ in range(size + 1)] for _ in range(size)]
    reduced_vector = [0.0 for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if i == j:
                reduced_matrix[i][j] = 0
            else:
                reduced_matrix[i][j] = - (diagonal_matrix[i][j] / diagonal_matrix[i][i])
        reduced_matrix[i][size] = diagonal_vector[i] / diagonal_matrix[i][i]
        reduced_vector[i] = diagonal_vector[i] / diagonal_matrix[i][i]
    # теперь у нас есть приведенная система (все разделили на Аii и занулили элементы где i==j)
    diagonal_vector_new = [0.0 for _ in range(size)]
    prom_vector_accuracy = [sys.float_info.max for _ in range(size)]
    while max(prom_vector_accuracy) >= accuracy:
        iteration_count += 1
        for i in range(size):
            prom = 0
            for j in range(size):
                prom += reduced_matrix[i][j] * reduced_vector[j]
            prom += reduced_matrix[i][size]
            diagonal_vector_new[i] = prom
        for i in range(size):
            prom_vector_accuracy[i] = abs(diagonal_vector_new[i] - reduced_vector[i])
        for i in range(size):
            reduced_vector[i] = diagonal_vector_new[i]

    # Формируем строку ответа

    result = ""
    for i in range(size):
        result += "X" + str(i + 1) + " = " + str(round(diagonal_vector_new[i], rnd)) + "\n"
    result += "\nОтвет был достигнут за число итераций = " + str(iteration_count) + "\n"
    result += "\nПогрешности:\n"
    for i in range(size):
        result += "X" + str(i + 1) + " = " + str(round(prom_vector_accuracy[i], rnd_accuracy)) + "\n"
    show_answer(result, matrix, vector, size, accuracy)


def calculate_determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for i in range(len(matrix)):
        minor = [row[:i] + row[i + 1:] for row in matrix[1:]]
        sign = (-1) ** i
        det += sign * matrix[0][i] * calculate_determinant(minor)

    return det
    # copied_matrix = copy_matrix(matrix)
    # n = len(copied_matrix)
    # det = 1
    #
    # for i in range(n):
    #     if copied_matrix[i][i] == 0:
    #         for j in range(i + 1, n):
    #             if copied_matrix[j][i] != 0:
    #                 copied_matrix[i], copied_matrix[j] = copied_matrix[j], copied_matrix[i]
    #                 det *= -1
    #                 break
    #     else:
    #         return 0
    #     det *= copied_matrix[i][i]
    #     for j in range(i + 1, n):
    #         coef = copied_matrix[j][i] / copied_matrix[i][i]
    #         for k in range(i, n):
    #             copied_matrix[j][k] -= coef * copied_matrix[i][k]
    #
    # return det


def copy_matrix(matrix):
    copy = [row[:] for row in matrix]
    return copy


def diagonal_dominance(matrix, size, vector, accuracy):
    matrix_diagonal = [[0 for _ in range(size)] for _ in range(size)]
    vector_diagonal = [0 for _ in range(size)]
    index_array = [-1 for _ in range(size)]
    for i in range(size):
        maximum = sys.float_info.min
        max_index = 0
        for j in range(size):
            if maximum < abs(matrix[i][j]):
                maximum = abs(matrix[i][j])
                max_index = j
        max_of_values = 0
        for j in range(size):
            if j != max_index:
                max_of_values += abs(matrix[i][j])
        if max_of_values > maximum or max_index in index_array:
            show_answer("\nВ СЛАУ нет диагонального преобладания!", matrix, vector, size, accuracy)
            return

        index_array[i] = max_index
        vector_diagonal[max_index] = vector[i]
        matrix_diagonal[max_index] = matrix[i]
    return matrix_diagonal, vector_diagonal
