import math
a= int(input("enter phy mark:"))
b= int(input("enter chem mark:"))
c= int(input("enter eco mark:"))

total= a+b+c
if(((a+b+c)/3)>=40):
    print("passed")

else:
    print("failed")

