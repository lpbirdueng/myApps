from functools import reduce
def prod(L):
    return reduce(lambda x, y:x*y, L)
print(prod([1,3,5,7,9]))