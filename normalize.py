
def normalize(name):
    norm_words = name[0].upper() + name[1:].lower()
    return norm_words
L1 = ['adam','LiSA','barT']
L2 = list(map(normalize,L1))
print(L2)