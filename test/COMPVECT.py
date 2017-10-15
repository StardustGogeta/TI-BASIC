from math import *
def disp(*args):
        print(" ".join(str(int(arg) if type(arg) == float and arg % 1 == 0 else arg) for arg in args))

disp("ANGLE=")
user = float(input("A=?"))
A= int(user) if not user % 1 else user
disp("MAGNITUDE=")
user = float(input("M=?"))
M= int(user) if not user % 1 else user
disp("X=",M*cos(A))
disp("Y=",M*sin(A))