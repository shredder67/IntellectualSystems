# Задача о назначениях https://en.wikipedia.org/wiki/Assignment_problem
# Датасет взят здесь http://people.brunel.ac.uk/~mastjjb/jeb/orlib/assigninfo.html


import pandas as pd
from math import exp, log
from random import random, randint, shuffle

import data_service as ds 


# Целевая функция, которую нужно минимизировать
def E(assignments, costs) -> float:
    value = 0
    for i in range(len(assignments)):
        value += costs[assignments[i]][i]
    return value


# Функция понижения температуры
def T(t):
    k = 0.5
    return t / (1 + k * t)


# Функция генерации следующего состояния системы
def G(x, t):
    i = randint(0, len(x) - 1)
    j = randint(0, len(x) - 1)

    new_x = x.copy()
    new_x[i], new_x[j] = new_x[j], new_x[i]
    return new_x


# Функция вероятности перехода к следующему состоянию
def h(d_E, t) -> float:
    if d_E < 0:
        return 1
    return exp(-d_E/t)


def check_prob(v) -> bool:
    return random() < v


def main():
    path, ans = ds.get_parsed_args()
    costs = pd.DataFrame.from_records([row for row in ds.read_data_by_rows(path)])

    # i-тый столбец содержит стоимость назначения i-того водителя ко всем пассажирам

    cur_solution = list(range(len(costs[0])))  # i - пассажир, solution[i] - водитель
    shuffle(cur_solution)
    f = E(cur_solution, costs)

    f_global_min = f
    temp = 100_000_000
    i = 1
    while temp > 0.01:
        if f_global_min > f:
            f_global_min = f
            print(f_global_min) 

        new_solution = G(cur_solution, temp)
        f_new = E(new_solution, costs)

        if check_prob(h(f_new - f, temp)):
            cur_solution = new_solution
            f = f_new

        if i % 15 == 0:
            temp = T(temp)
        i += 1

    print(f_global_min)
    if ans is not None:
        print("Правильный ответ:", ans)


if __name__ == '__main__':
    main()
