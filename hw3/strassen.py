import numpy as np


def split(a, n1):
    a1, a2 = np.vsplit(a, 2)
    a11, a12 = np.hsplit(a1, 2)
    a21, a22 = np.hsplit(a2, 2)
    return a11, a12, a21, a22


def merge(a11, a12, a21, a22):
    a1 = np.hstack((a11, a12))
    a2 = np.hstack((a21, a22))
    return np.vstack((a1, a2))


def multiply(a, b):
    n = a.shape[0]
    if n == 1:
        return np.dot(a, b)
    a11, a12, a21, a22 = split(a, n // 2)
    b11, b12, b21, b22 = split(b, n // 2)
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
    new_a = np.zeros((N, N))
    for i in range(n):
        for j in range(n):
            new_a[i][j] = a[i][j]
    return new_a


def get_right_size(n):
    k = 1
    while k < n:
        k *= 2
    return k


def main():
    n = int(input())
    a, b = np.empty((n, n), dtype=int), np.empty((n, n), dtype=int)
    for i in range(n):
        a[i] = np.array(list(map(int, input().split())))
    for i in range(n):
        b[i] = np.array(list(map(int, input().split())))

    N = get_right_size(n)
    c = multiply(resize(a, n, N), resize(b, n, N))
    print()
    for i in range(n):
        for j in range(n):
            print(int(c[i][j]), end=' ')
        print()

main()
