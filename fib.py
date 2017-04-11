def fib(max):
    n=0
    a=0
    b=1
    while n < max:
        #print(b)
        yield b
        #print(b)
        #a = b
        #b = a+b
        a,b = b, a+b
        n=n+1
    return 'done'
f= fib(100)
next(f)