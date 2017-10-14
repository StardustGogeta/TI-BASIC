from math import *
user = float(input("X=?"))
X= int(user) if not user % 1 else user
while X:
    print("HELLO WORLD",X)
    X=X-1