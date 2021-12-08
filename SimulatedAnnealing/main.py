# Задача о назначениях https://en.wikipedia.org/wiki/Assignment_problem
# Датасет взят здесь http://people.brunel.ac.uk/~mastjjb/jeb/orlib/assigninfo.html


from argparse import ArgumentParser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import data_service as ds 


# Целевая функция, которую нужно минимизировать
def E(assignments):
    return sum(assignments)

# Функция понижения температуры
def T(t):
    return t/2

# Функция генерации следующего состояния системы
def G(x, t):
    pass

# Функция вероятности перехода к следующему состоянию
def h(d_E, t):
    pass


def main():
    path, ans = ds.get_parsed_args()
    data = pd.DataFrame.from_records([row for row in ds.read_data_by_rows(path)])
    print(data)
    

if __name__ == '__main__':
    main()