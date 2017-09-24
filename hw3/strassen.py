import numpy as np
from math import log, ceil


def split(a):
    a1, a2 = np.vsplit(a, 2)
    a11, a12 = np.hsplit(a1, 2)
    a21, a22 = np.hsplit(a2, 2)
    return a11, a12, a21, a22


def merge(a11, a12, a21, a22):
    a1 = np.hstack((a11, a12))
    a2 = np.hstack((a21, a22))
    return np.vstack((a1, a2))


def multiply(a, b):
    if a.shape[0] == 1:
        return np.dot(a, b)
    a11, a12, a21, a22 = split(a)
    b11, b12, b21, b22 = split(b)
    p1 = multiply(a11 + a22, b11 + b22)
    p2 = multiply(a21 + a22, b11)
    p3 = multiply(a11, b12 - b22)
    p4 = multiply(a22, b21 - b11)
    p5 = multiply(a11 + a12, b22)
    p6 = multiply(a21 - a11, b11 + b12)
    p7 = multiply(a12 - a22, b21 + b22)
    c = merge(p1 + p4 - p5 + p7, p3 + p5, p2 + p4, p1 - p2 + p3 + p6)
    return c


def resize(a, n, N):
    return np.pad(a, (0, N - n), 'constant', constant_values=(0))


def read_array(n):
    return np.array([list(map(int, input().split())) for i in range(n)], dtype=int)


def print_array(a, n):
    print()
    for i in range(n):
        for j in range(n):
            print(int(a[i][j]), end=' ')
        print()


def main():
    n = int(input())
    a, b = read_array(n), read_array(n)

    N = 2 ** (ceil(log(n, 2)))
    print_array(multiply(resize(a, n, N), resize(b, n, N)), n)


if __name__ == '__main__':
    main()
