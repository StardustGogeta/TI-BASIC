from math import *
def disp(*args):
        print(" ".join(str(int(arg) if type(arg) == float and arg % 1 == 0 else arg) for arg in args))

user = float(input("X=?"))
X= int(user) if not user % 1 else user
while X:
    disp("HELLO WORLD",X)
    X=X-1