from math import *
def disp(*args):
        print(" ".join(str(int(arg) if type(arg) == float and arg % 1 == 0 else arg) for arg in args))

user = float(input("X=?"))
X= int(user) if not user % 1 else user
user = float(input("Y=?"))
Y= int(user) if not user % 1 else user
disp("VELOCITY?")
user = float(input("A=?"))
A= int(user) if not user % 1 else user
if A>0:
    user = float(input("V=?"))
    V= int(user) if not user % 1 else user
    disp("ANGLE=",round(9.81*sqrt(X**2+Y**2)/V**2/2, 2))
else:
    user = float(input("θ=?"))
    θ= int(user) if not user % 1 else user
    disp("VELOCITY=",round(sqrt(9.81*sqrt(X**2+Y**2)/sin(2*θ)), 2))
disp("RANGE=",round(sqrt(X**2+Y**2), 2))