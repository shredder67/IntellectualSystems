# Задача о назначениях https://en.wikipedia.org/wiki/Assignment_problem
# Датасет взят здесь http://people.brunel.ac.uk/~mastjjb/jeb/orlib/assigninfo.html


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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
    print("Hello world!")

if __name__ == '__main__':
    main()