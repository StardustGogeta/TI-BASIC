from math import *
def disp(*args):
        print(" ".join(str(int(arg) if type(arg) == float and arg % 1 == 0 else arg) for arg in args))

user = float(input("A=?"))
A= int(user) if not user % 1 else user
D=1
while sqrt(A)>=D:
    if A % D==0:
        disp(D,A/D)
    D=D+1
disp("LIST COMPLETE")