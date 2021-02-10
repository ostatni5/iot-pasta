import numpy as np


# functions
def s_sin(t):
    return 0.003*np.sin(3.14*t)

def s_tsin(t):
    return 0.05*0.1*(t)*np.sin(3.14*t) + 0.02*np.sin(20*t)

def s_logexp(t):
    if isinstance(t, float) and t < 20:
        return 0.003*np.sin(3.14*t)
    return 1/(1+np.exp((-t+20)*0.01))*np.sin(4*t)

def s_logexp2(t):
    if isinstance(t, float) and t < 20:
        return 0.003*np.sin(3.14*t)
    elif isinstance(t, float) and t < 100:
        return 1/(1+np.exp((-t+20)*0.01))*np.sin(4*t)
    return 0.003*np.sin(3.14*t)

def s_sin2(t):
    return 0.0000001*np.sin(100000000*t**4)*t

def s_sin2(t):
    return 0.0003*np.sin(40*t**4)*0.001*t


#
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



s_f = s_sin # deviation function
v_f = lambda x: v(s_f, x)
a_f = lambda x: a(v_f, x)