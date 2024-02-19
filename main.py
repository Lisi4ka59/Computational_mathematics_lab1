import tkinter as tk
from tkinter import messagebox
from calculating import calculate_matrix

# Создание списка для хранения переменных, связанных с entry_matrix
entries = []
entries_vector = []
check_det = False


def input_matrix_values():
    try:
        try:
            matrix = [[0 for _ in range(size)] for _ in range(size)]
            vector = []
            count = 0
            for entr in entries:
                value = float(entr.get())
                matrix[count // size][count % size] = value
                count += 1
            for entr in entries_vector:
                value = float(entr.get())
                vector.append(value)
            print(check_det)
            calculate_matrix(matrix, vector, size, accuracy, check_det)
        except ValueError:
            messagebox.showerror("418", "I'm a teapot, please make sure your entered values have the right format!")
    except IndexError:
        messagebox.showerror("418", "I'm a teapot, please make sure your entered correct number of values!")


def input_matrix() -> None:
    input_matrix_size_button.pack_forget()
    entry.pack_forget()
    label_size.pack_forget()
    label_accuracy.pack_forget()
    entry_accuracy.pack_forget()
    label_check.pack_forget()
    input_check_button.pack_forget()
    label_check_dop.pack_forget()

    root.title("Ввод матрицы " + str(size) + "х" + str(size))

    for i in range(size):
        for j in range(size):
            entry_var = tk.StringVar()
            entry_matrix = tk.Entry(root, width=6, textvariable=entry_var)
            entry_matrix.grid(row=i, column=j, padx=5, pady=5)
            entries.append(entry_var)

    for i in range(size):
        entry_var = tk.StringVar()
        entry_matrix = tk.Entry(root, width=8, textvariable=entry_var)
        entry_matrix.grid(row=i, column=size, padx=5, pady=5)
        entries_vector.append(entry_var)

    submit_button = tk.Button(root, text="Решить", command=input_matrix_values, width=6)
    submit_button.grid(row=size, column=size // 2)


def on_input_matrix_size_click():
    global size
    size = 0
    input_value = entry.get()
    global accuracy

    try:
        accuracy = float(entry_accuracy.get())
        size = int(input_value)
        if 2 <= size <= 20:
            input_matrix()
        else:
            messagebox.showwarning("Неверный ввод",
                                   "Размерность матрицы должна быть от 2 до 20. Пожалуйста, введите корректное число.")
    except ValueError:
        messagebox.showerror("Ошибка", "Введено некорректное значение. Пожалуйста, введите целое число.")


# Создаем функции для обработки нажатия кнопок
def on_input_keyboard_button_click():
    input_keyboard_button.pack_forget()  # скрываем первую кнопку
    input_file_button.pack_forget()  # скрываем вторую кнопку
    label_size.pack()
    entry.pack()
    label_accuracy.pack()
    # показываем поле для ввода числа
    # Создаем кнопки
    entry_accuracy.pack()
    input_matrix_size_button.pack()
    label_check.pack()
    input_check_button.pack()
    label_check_dop.pack()


def on_check_click():
    check_change(check_det)
    input_check_button.config(text="включено" if check_det else "выключено")


def check_change(check):
    global check_det
    check_det = not check
    return check_det


def on_file_button_click():
    file_name = str(entry_file_name.get()) + ".txt"
    if file_name == ".txt":
        file_name = "input.txt"
    try:
        try:
            try:
                with (open(file=file_name, mode="r", encoding="utf-8") as file):
                    vector = []
                    from_file_size = int(file.readline())
                    from_file_accuracy = float(file.readline())
                    from_file_input = file.readline()
                    from_file_check_determinant = True if "true" in from_file_input or "True" in from_file_input else False
                    print(from_file_check_determinant)
                    matrix = [[0 for _ in range(from_file_size)] for _ in range(from_file_size)]
                    for i in range(from_file_size):
                        input_line = file.readline().split(" ")
                        for j in range(from_file_size):
                            matrix[i][j] = float(input_line[j])
                        vector.append(float(input_line[from_file_size]))
                    calculate_matrix(matrix, vector, from_file_size, from_file_accuracy, from_file_check_determinant)
            except FileNotFoundError:
                messagebox.showerror("418", "Can not find file!")

        except ValueError:
            messagebox.showerror("418", "I'm a teapot, please make sure your entered values have the right format!")

    except IndexError:
        messagebox.showerror("418", "I'm a teapot, please make sure your entered correct number of values!")


def on_input_file_button_click():
    input_keyboard_button.pack_forget()
    input_file_button.pack_forget()

    entry_file_name.pack()
    input_file_name_button = tk.Button(root, text="Найти файл", command=on_file_button_click, width=15)
    input_file_name_button.pack()


# Создаем главное окно
root = tk.Tk()
root.minsize(300, 200)
root.title("Калькулятор СЛАУ методом простых итераций")

# Создаем кнопки
input_keyboard_button = tk.Button(root, text="Ввод с клавиатуры", command=on_input_keyboard_button_click, width=15)

input_file_button = tk.Button(root, text="Ввод из файла", command=on_input_file_button_click, width=15)

input_matrix_size_button = tk.Button(root, text="Ввод", command=on_input_matrix_size_click,
                                     width=20, height=1)

input_keyboard_button.pack()
input_file_button.pack()

entry = tk.Entry(root)  # поле для ввода числа, изначально скрытое
entry.pack_forget()
entry_file_name = tk.Entry(root)
entry_file_name.pack_forget()
entry_accuracy = tk.Entry(root)
entry_accuracy.pack_forget()
label_size = tk.Label(root, text="Введите размер матрицы")
label_size.pack_forget()
label_accuracy = tk.Label(root, text="Введите точность подсчета")
label_accuracy.pack_forget()
label_check = tk.Label(root, text="Проверка, что определитель матрицы не равен нулю")
label_check.pack_forget()
label_check_dop = tk.Label(root, text="(не рекомендуется при большой размерности матрицы)")
label_check_dop.pack_forget()

# callback = (on_check_click(check_det), '%P')
input_check_button = tk.Button(root, text="выключено", command=on_check_click,
                               width=15, height=1)
input_check_button.pack_forget()

# Запускаем главный цикл обработки событий
root.mainloop()
