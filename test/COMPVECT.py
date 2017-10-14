from math import *
print("ANGLE=")
user = float(input("A=?"))
A= int(user) if not user % 1 else user
print("MAGNITUDE=")
user = float(input("M=?"))
M= int(user) if not user % 1 else user
print("X=",M*cos(A))
print("Y=",M*sin(A))