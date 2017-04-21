import random
class Coin:
    def __init__(self):
        self.coin = [0,1]
    
    def __call__(self):
        return random.choice(self.coin)
    
    def throw(self, times=1):
        n0 = 0
        n1 = 0
        for n in range(times):
            result = self.__call__()
            if result == 1:
                n1 = n1+1
            if result == 0:
                n0 = n0 + 1
        print('1= ', n1)
        print('0= ', n0)
        return(n1/times)
    def throw_all(self, times=1):
        n0 = 0
        n1 = 0
        r = []
        for n in range(times):
            result = self.__call__()
            if result == 1:
                n1 = n1+1
            if result == 0:
                n0 = n0 + 1
            r.append((n1/(n+1)))
        return r
    
if __name__ == '__main__':
    c = Coin()
    value1 = 0
    value2 = 0
    n1 = 0
    r = 0
    times = 1000000
    for n in range(times):
        result = c()
        if 0.8 < r < 1:
            if result == 1:
                value1 = value1 - 1
            if result == 0:
                value1 = value1 + 1
        if 0< r < 0.2:
            if result == 1:
                value1 = value1 + 1
            if result == 0:
                value1 = value1 - 1            
        if result == 1:
            n1 = n1 + 1
            value2 = value2 + 1
        if result == 0:
            value2 = value2 - 1
        r = n1/(n+1)            
    print("value1 = ", value1)
    print("value2 = ", value2)
    #print("r = ", r)
    #print("n1 = ", n1)
    print("gap = ", (n1-(times - n1)))
    #r=c.throw(10)
    #print(r)
    """
    result = c.throw_all(100000)
    for row in result:
        with open('coin.txt', 'a', newline='\r\n') as f:
            f.write(str(row)+'\n')
    """