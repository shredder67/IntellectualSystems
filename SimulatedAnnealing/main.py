# Задача о назначениях https://en.wikipedia.org/wiki/Assignment_problem
# Датасет взят здесь http://people.brunel.ac.uk/~mastjjb/jeb/orlib/assigninfo.html

from matplotlib import pyplot as plt
import pandas as pd
from math import exp, log
from random import random, randint, shuffle

import data_service as ds 


# Целевая функция, которую нужно минимизировать
def E(assignments, costs) -> float:
    value = 0
    for i in range(len(assignments)):
        value += costs[i][assignments[i]]
    return value


# Функция понижения температуры
def T(t):
    k = 0.99
    return k * t


# Функция вероятности перехода к следующему состоянию
def h(d_E, t) -> float:
    if d_E < 0:
        return 1
    return exp(-d_E/t)


# Проверка перехода в новое состояние
def check_prob(v) -> bool:
    return random() < v


# Метод отжига
def anneal():
    path, ans = ds.get_parsed_args()
    costs = pd.DataFrame.from_records([row for row in ds.read_data_by_rows(path)])

    # i-тая строка содержит стоимость назначения i-того водителя ко всем пассажирам

    cur_solution = list(range(len(costs[0])))  # s[i] = j : i-тый водитель j-тому пассажиру
    shuffle(cur_solution)
    f = E(cur_solution, costs)

    f_global_min = f
    max_temp = 10_000
    temp = max_temp
    k = 1
    y_values = []
    while temp > 0.1:
        if f_global_min > f:
            f_global_min = f


        while True:
            i = randint(0, len(cur_solution) - 1)
            j = randint(0, len(cur_solution) - 1)
            cur_solution[i], cur_solution[j] = cur_solution[j], cur_solution[i]
            cur_solution[i:j + 1]
            f_new = E(cur_solution, costs)
            prob = h(f_new - f, temp)

            if check_prob(prob):
                f = f_new
                break
            else:
                cur_solution[i], cur_solution[j] = cur_solution[j], cur_solution[i]

        y_values.append(f)
        temp = T(temp)
        k += 1

    print(k)
    print(f_global_min)
    if ans is not None:
        print("Правильный ответ:", ans)

    return list(range(k - 1)), y_values


def main():
    x,y = anneal()
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    main()
