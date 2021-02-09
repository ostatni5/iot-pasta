import numpy as np


def s(t):
    return np.sin(t)

def s2(t):
    return np.sin(t)+np.cos(t)

def s3(t):
    return t**2


def v(s, t):
    h = 0.001
    return (s(t+h) - s(t-h))/(2*h)
def a(v, t):
    h = 0.001
    return (v(t+h) - v(t-h))/(2*h)

def integral(func, x_start, x_end):
    sum = 0
    step = (x_end - x_start) / 10
    x = x_start
    while x < x_end:
        x2 = x + step/2
        sum += step * func(x2)
        x += step
    return sum

def rms(func, t_start, t_end):
    integr = integral(lambda x: func(x)**2, t_start,t_end)
    return np.sqrt(integr/(t_end - t_start))

def peak(func, t_start, t_end):
    x = np.arange(t_start, t_end, 0.05)
    y = func(x)
    return np.max(y) - np.min(y)