from math import sqrt
def same(x=[],*func):
    s=[f(x_k) for x_k in x for f in func]
    return s
print(same([8,16,25,9],sqrt,abs))