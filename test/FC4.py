from math import *
user = float(input("A=?"))
A= int(user) if not user % 1 else user
D=1
while sqrt(A)>=D:
    if A % D==0:
        print(D,A/D)
    D=D+1
print("LIST COMPLETE")