__author__ = 'Palmira Pereira'
from scipy.spatial import Delaunay
import numpy as np
import random
import math

lam= 5 # mean and standard deviation
s = np.random.normal(25,7,800)
p = np.random.normal(25,7,800)

points3=[]
a=65.0
b=1
k=40.0


for i in range(int(a)+1):
    for j in range(int(a)+1):

        if i%2==0:
            points3.append([(i/a)**b*k+(random.randrange(0, 201,1)-100)/10/a,(j/a)**b*k+(random.randrange(0, 201,1)-100)/10/a])
        else:
            points3.append([(i/a)**b*k+(random.randrange(0, 201,1)-100)/10/a,(j/a+1*0.5/a)**b*k+(random.randrange(0, 201,1)-100)/10/a])
'''
points3=[]
for i in range(int(a)+1):
    for j in range(int(a)+1):


        points3.append([k*i/a,k*j/a])

'''
tri = Delaunay(points3)
temp=tri.simplices
print(tri.simplices)
print(points3[1][0])
text_file = open("delaunay.dat", "w")


text_file.write("TITLE=\"TRIANGLE UPLOAD NEW\"\n")
text_file.write("VARIABLES= \"X\",\"Y\"\n")
text_file.write("ZONE\nDataPacking=Block\nZoneType=FETRIANGLE\n")
text_file.write("N=")
text_file.write(str(len(points3)))
text_file.write(" E=")
text_file.write(str(len(temp)))
text_file.write("\n")
for i in range(len(points3)):
    text_file.write (str(points3[i][0])+" ")
text_file.write("\n")
for i in range(len(points3)):
    text_file.write (str(points3[i][1])+" ")
text_file.write("\n")
for i in temp:
    text_file.write(str(i[0]+1)+" "+str(i[1]+1)+" "+str(i[2]+1))
    text_file.write("\n")



text_file = open("random_x.dat", "w")

for i in range(len(points3)-1):
    text_file.write (str(points3[i][0])+",")
text_file.write (str(points3[len(points3)-1][0]))


text_file = open("random_y.dat", "w")
for i in range(len(points3)-1):
    text_file.write (str(points3[i][1])+",")
text_file.write (str(points3[len(points3)-1][1]))
text_file.write("\n")
