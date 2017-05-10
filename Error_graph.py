__author__ = 'Palmira Pereira'
from math import *
import random
import numpy as np
from scipy.spatial import Delaunay

def Dot(u,v):
    # Find the dot product of vector u and v
    return u.x*v.x+v.y*u.y
def Length(u):
    # Finds the length of vector u
    return (u.x**2+u.y**2)**0.5
def Cross_product(u,v):
    # UcrossV
    return u.x*v.y-u.y*v.x

# All the different classes
class edge(object):
    def __init__(self,points,point_list):
        self.point=[points[point_list[0]],points[point_list[1]]]
    def length(self):
        return abs(Length(self.point[0]-self.point[1]))
    def mid_point(self):
        return vector((self.point[1].x-self.point[0].x)*0.5,(self.point[1].y-self.point[0].y)*0.5)
class triangle(object):
    def __init__(self,points,point_list):
        self.point=[points[point_list[0]],points[point_list[1]],points[point_list[2]]]
    def centroid (self):
        return vector((self.point[1].x+self.point[0].x+self.point[2].x)/3.0,(self.point[1].y+self.point[0].y+self.point[2].y)/3.0)
class unstructured_mesh(object):
    def __init__(self,points):
        self.points=points
    def triangles(self):
        points=self.points
        points2=[]
        for i in points:
            points2.append([i.x,i.y])
        tri = Delaunay(points2)
        temp=tri.simplices
        temp2=[]
        for i in temp:
            temp2.append([i[0],i[1],i[2]])
        return temp2
class vector(object):
    def __init__(self,x,y):
        self.x=float(x)
        self.y=float(y)
    def __add__(self,v):
        return vector(self.x + v.x, self.y + v.y )
    def __sub__(self,v):
        return vector(self.x - v.x, self.y - v.y )
    def __mul__(self,val):
        return vector(val*self.x,val*self.y)


def find_center_of_circle():
    # Finds where to center the circle
    return vector(20,20)
    #return vector(20+(random.randrange(0, 201,1)-100)/100.0,20+(random.randrange(0, 201,1)-100)/100.0)
def intersection_line_line(v1,v2,u1,u2):
    # Finds the intersection of two lines defined by the points (v1,v2) and (u1,u2)
    # Returns the point of intersection or returns false if the lines do not intersect
    if u1.x == u2.x:
        b2 = u1.x
        if v1.x == v2.x:
            return False
        else:
            m1 = (v2.y-v1.y)/(v2.x-v1.x)
            b1 = v2.y-m1*v2.x
            intersection_point = vector(b2,m1*b2+b1)
            if abs(Length(v2-v1)-Length(v2-intersection_point)-Length(v1-intersection_point))<0.000001 and abs(Length(u2-u1)-Length(u2-intersection_point)-Length(u1-intersection_point))<0.000001:
                return intersection_point
            else:
                return False
    elif v1.x == v2.x:
        b1 = v1.x
        m2 = (u2.y-u1.y)/(u2.x-u1.x)
        b2 = u2.y-m2*u2.x
        intersection_point = vector(b1,m2*b1+b2)
        if abs(Length(v2-v1)-Length(v2-intersection_point)-Length(v1-intersection_point))<0.000001 and abs(Length(u2-u1)-Length(u2-intersection_point)-Length(u1-intersection_point))<0.000001:
            return intersection_point
        else:
            return False
    else:
        m1 = (v2.y-v1.y)/(v2.x-v1.x)
        m2 = (u2.y-u1.y)/(u2.x-u1.x)
        if m1 == m2:
            return False
        b1 = v2.y-m1*v2.x
        b2 = u2.y-m2*u2.x
        x = (b2-b1)/(m1-m2)
        y = m1*x+b1
        intersection_point = vector(x,y)
        if abs(Length(v2-v1)-Length(v2-intersection_point)-Length(v1-intersection_point))<0.0000001 and abs(Length(u2-u1)-Length(u2-intersection_point)-Length(u1-intersection_point))<0.0000001:
            return intersection_point
        else:
            return False
def sort_counterclockwise(middle,points_around):
    # Sorts points counterclockwise between the middle point
    points_around_polar=[]
    for i in range(len(points_around)):
        points_around[i]=points_around[i]-middle

    for i in points_around:
        if i.x==0 and i.y>0:
            temp_angle=pi*0.5
            temp_radius=i.y
        elif i.x==0 and i.y==0:
            temp_angle=0
            temp_radius=0
        elif i.x==0 and i.y<0:
            temp_angle=pi*3*0.5
            temp_radius=-i.y
        elif i.x>0 and i.y==0:
            temp_angle=0
            temp_radius=i.x
        elif i.x<0 and i.y==0:
            temp_angle=pi
            temp_radius=-i.x
        elif i.x>0 and i.y>0:
            temp_angle=atan(i.y/i.x)
            temp_radius=Length(i)
        elif i.x<0 and i.y>0:

            temp_angle=pi-atan(-i.y/i.x)
            temp_radius=Length(i)
        elif i.x<0 and i.y<0:
            temp_angle=pi+atan(i.y/i.x)
            temp_radius=Length(i)
        else:
            temp_angle=2*pi-atan(-i.y/i.x)
            temp_radius=Length(i)
        points_around_polar.append([temp_angle,temp_radius])
    index=[]
    temp_index=0
    temp_closest=[[2*pi,5]]
    for j in points_around_polar:
        temp_closest[0]=2*pi
        for i in range(len(points_around_polar)):
            temp_point=points_around_polar[i]
            if i not in index:
                if temp_point[0]<temp_closest[0]:
                    temp_closest[0]=temp_point[0]
                    temp_index=i
        index.append(temp_index)
    points_around_sorted=[]
    points_around_sorted.append(middle)
    for i in index:
        if Length(points_around[i])>0.00000001:
            points_around_sorted.append(points_around[i]+middle)

    return(points_around_sorted)
def create_points():
    # Reads points from the textfile generated by the file Test_delaunay and returns these points
    text_file = open("random_x.dat", "r")
    s = text_file.read().split(',')
    text_file.close()
    text_file = open("random_y.dat", "r")
    p = text_file.read().split(',')
    text_file.close()
    points=[]
    for i in range(len(s)):
        points.append(vector(s[i],p[i]))
    return points
def area_polygon(middle,sorted):
    # Finds the area of the polygon formed by the given sorted points
    total_area=0
    for i in range(len(sorted)-1):
        total_area=total_area+area([middle,sorted[i],sorted[i+1]])
    return (total_area)
def create_text(points,triangles,volume_fraction,normal_x,normal_y,all_rectangle_points,error_curvature,curvature,new_volume_fraction):
    # Creates a textfile to plot on tecplot
    text_file = open("triangle_upload_new.dat", "w")
    text_file.write("TITLE=\"TRIANGLE UPLOAD NEW\"\n")
    text_file.write("VARIABLES= \"X\",\"Y\",\"Volume Fraction\",\"U\",\"V\",\"Curvature\",\"Curvature Error\",\"CellNumber\"\n")
    text_file.write("ZONE\nDataPacking=Block\nZoneType=FETRIANGLE\n")
    text_file.write("N=")
    text_file.write(str(len(points)))
    text_file.write(" E=")
    text_file.write(str(len(triangles)))
    text_file.write("\nVARLOCATION=([3-8]=CELLCENTERED)\n")
    for i in range(len(points)):
        text_file.write (str(points[i].x)+" ")
    text_file.write ("\n")
    for i in range(len(points)):
        text_file.write (str(points[i].y)+" ")
    text_file.write ("\n")
    for i in range(len(volume_fraction)):
        text_file.write (str(new_volume_fraction[i])+" ")
    text_file.write ("\n")
    for i in range(len(normal_x)):
        text_file.write (str(normal_x[i])+" ")
    text_file.write ("\n")
    for i in range(len(normal_y)):
        text_file.write (str(normal_y[i])+" ")
    text_file.write ("\n")
    counter=0
    for i in range(len(volume_fraction)):
        if volume_fraction[i]!=0 and volume_fraction[i]!=1:
            text_file.write (str(curvature[counter])+" ")
            counter=counter+1
        else:
            text_file.write (str(0)+" ")
    text_file.write ("\n")
    counter=0
    for i in range(len(volume_fraction)):
        if volume_fraction[i]!=0 and volume_fraction[i]!=1:
            text_file.write (str(error_curvature[counter])+" ")
            counter=counter+1
        else:
            text_file.write (str(0)+" ")
    text_file.write ("\n")
    for i in range(len(normal_y)):
        text_file.write (str(i)+" ")
    text_file.write ("\n")
    for i in range(len(triangles)):
        temp_triangle=triangles[i]
        for j in range(3):
            text_file.write (str(temp_triangle[j]+1)+" ")
        text_file.write ("\n")

    '''
    ##extra zone for rectangle
    text_file.write("ZONE\nDataPacking=Block\nZoneType=FEQUADRILATERAL\n")
    text_file.write("N=")
    text_file.write(str(len(all_rectangle_points)*4))
    text_file.write(" E=")
    text_file.write(str(len(all_rectangle_points)))
    text_file.write("\nVARLOCATION=([3-8]=CELLCENTERED)\n")
    for i in all_rectangle_points:
        for j in range(4):
            text_file.write(str(i[j].x)+" ")
    text_file.write ("\n")
    for i in all_rectangle_points:
        for j in range(4):
            text_file.write(str(i[j].y)+" ")
    text_file.write ("\n")
    for i in range(len(all_rectangle_points)):
        text_file.write("4 ")
    text_file.write ("\n")
    for i in range(len(all_rectangle_points)):
        text_file.write("4 ")
    text_file.write ("\n")
    for i in range(len(all_rectangle_points)):
        text_file.write("4 ")
    text_file.write ("\n")
    for i in range(len(all_rectangle_points)):
        text_file.write("4 ")
    text_file.write ("\n")
    for i in range(len(all_rectangle_points)):
        text_file.write("4 ")
    text_file.write ("\n")
    for i in range(len(all_rectangle_points)):
        text_file.write("1 ")
    text_file.write ("\n")
    for i in range(len(all_rectangle_points)*4):
        if (i+1)%4==0:
            text_file.write(str(i+1))
            text_file.write ("\n")
        else:
            text_file.write(str(i+1)+" ")
    '''

    for j in range(len(all_rectangle_points)):

        if j%3==0:
            w=all_rectangle_points[j]
            text_file.write("ZONE\nDataPacking=Block\nZoneType=FEQUADRILATERAL\n")
            text_file.write("N=")
            text_file.write(str(12))
            text_file.write(" E=")
            text_file.write(str(3))
            text_file.write("\nVARLOCATION=([3-8]=CELLCENTERED)\n")
            for i in range(4):
                text_file.write(str(w[i].x)+" ")
            w=all_rectangle_points[j+1]
            for i in range(4):
                text_file.write(str(w[i].x)+" ")
            w=all_rectangle_points[j+2]
            for i in range(4):
                text_file.write(str(w[i].x)+" ")

            text_file.write ("\n")
            w=all_rectangle_points[j]
            for i in range(4):
                text_file.write(str(w[i].y)+" ")
            w=all_rectangle_points[j+1]
            for i in range(4):
                text_file.write(str(w[i].y)+" ")
            w=all_rectangle_points[j+2]
            for i in range(4):
                text_file.write(str(w[i].y)+" ")
            text_file.write ("\n")

            text_file.write(str(j)+" "+str(j)+" "+str(j))
            text_file.write ("\n")

            text_file.write("4 4 4 ")
            text_file.write ("\n")

            text_file.write("4 4 4")
            text_file.write ("\n")

            text_file.write("4 4 4 ")
            text_file.write ("\n")

            text_file.write("4 4 4")
            text_file.write ("\n")
            text_file.write("1 1 1")
            text_file.write ("\n")

            text_file.write("1 2 3 4 ")
            text_file.write ("\n")
            text_file.write("5 6 7 8 ")
            text_file.write ("\n")
            text_file.write("9 10 11 12 ")
            text_file.write ("\n")

    text_file.close()
def area(point):
    #Finds area of given triangle
    v1=point[1]-point[0]
    v2=point[2]-point[0]
    return abs(0.5*((v1.x*v2.y)-(v2.x*v1.y)))
def intersection_line_circle(u,v,radius,center_circle):
    # Finds the intersection between a line (defined by points u and v) and circle
    u=u-center_circle
    v=v-center_circle
    if u.x-v.x!=0:
        m=float((u.y-v.y)/(u.x-v.x))
        b=u.y-m*u.x
        x1=(-2*m*b-sqrt((2*m*b)**2-4*(1+m**2)*(b**2-radius**2)))*0.5/(1+m**2)
        temp_vector=vector(x1,x1*m+b)
        if (abs(Length(u-temp_vector)+Length(v-temp_vector)-Length(u-v)))<=0.0001:
            x2=(-2*m*b+sqrt((2*m*b)**2-4*(1+m**2)*(b**2-radius**2)))*0.5/(1+m**2)
            temp_vector=vector(x2,x2*m+b)
            if(abs(Length(u-temp_vector)+Length(v-temp_vector)-Length(u-v)))<=0.0001:
                return vector(x1,x1*m+b)+center_circle,vector(x2,x2*m+b)+center_circle
            else:
                return vector(x1,x1*m+b)+center_circle,-1
        else:
            x1=(-2*m*b+sqrt((2*m*b)**2-4*(1+m**2)*(b**2-radius**2)))*0.5/(1+m**2)
            temp_vector=vector(x1,x1*m+b)
            if (abs(Length(u-temp_vector)+Length(v-temp_vector)-Length(u-v)))<=0.0001:
                return vector(x1,x1*m+b)+center_circle,-1
            else:
                return vector(-1,-1)
    else:
        b=u.x
        y1=sqrt(radius**2-b**2)
        temp_vector=vector(b,y1)
        if (abs(Length(u-temp_vector)+Length(v-temp_vector)-Length(u-v)))<=0.0001:
            temp_vector=vector(b,-y1)
            if (abs(Length(u-temp_vector)+Length(v-temp_vector)-Length(u-v)))<=0.0001:
                return vector(b,y1)+center_circle,vector(b,-y1)+center_circle
            else:
                return vector(b,y1)+center_circle,-1
        else:
            temp_vector=vector(b,-y1)
            if (abs(Length(u-temp_vector)+Length(v-temp_vector)-Length(u-v)))<=0.0001:
                return vector(b,-y1)+center_circle,-1
            else:
                return vector(-1,-1)
def find_volume_fraction(points,triangles,radius,radius_vector):
    # Finds the volume fraction
    count=0
    #initializing array
    volume_fraction=[]
    total_area=[]
    for i in range(len(triangles)):
        volume_fraction.append(0)
        total_area.append(0)
    #triangles all in shape
    for i in range(len(triangles)):
        temp_triangle=triangles[i]
        if (Length(points[temp_triangle[0]]-radius_vector))<=radius and (Length(points[temp_triangle[1]]-radius_vector))<=radius and (Length(points[temp_triangle[2]]-radius_vector))<=radius:
            volume_fraction[i]=1
        total_area[i]=volume_fraction[i]*area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
    #triangles with one point in shape
    temp_approximate_triangle=[]

    for i in range(len(triangles)):
        temp_triangle=triangles[i]
        for j in range(3):
            if (Length(points[temp_triangle[j]]-radius_vector))<=radius:
                index=j
                count+=1
        if count==0:
            counter=0
            counter2=[]
            midpoint=vector((points[temp_triangle[0]].x+points[temp_triangle[1]].x)*0.5,(points[temp_triangle[0]].y+points[temp_triangle[1]].y)*0.5)

            if Length(midpoint-radius_vector)<radius:
                counter=counter+1
                temp_intersection=intersection_line_circle(points[temp_triangle[0]],points[temp_triangle[1]],radius,radius_vector)
                temp_angle=acos(Dot(temp_intersection[0]-radius_vector,temp_intersection[1]-radius_vector)/Length(temp_intersection[0]-radius_vector)/Length(temp_intersection[1]-radius_vector))
                volume_fraction[i]=((0.5)*radius*radius*(temp_angle-sin(temp_angle)))/area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
                counter2.append(volume_fraction[i])
            midpoint=vector((points[temp_triangle[0]].x+points[temp_triangle[2]].x)*0.5,(points[temp_triangle[0]].y+points[temp_triangle[2]].y)*0.5)

            if Length(midpoint-radius_vector)<radius :
                counter=counter+1
                temp_intersection=intersection_line_circle(points[temp_triangle[0]],points[temp_triangle[2]],radius,radius_vector)
                temp_angle=acos(Dot(temp_intersection[0]-radius_vector,temp_intersection[1]-radius_vector)/Length(temp_intersection[0]-radius_vector)/Length(temp_intersection[1]-radius_vector))
                volume_fraction[i]=((0.5)*radius*radius*(temp_angle-sin(temp_angle)))/area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
                counter2.append(volume_fraction[i])
            midpoint=vector((points[temp_triangle[1]].x+points[temp_triangle[2]].x)*0.5,(points[temp_triangle[1]].y+points[temp_triangle[2]].y)*0.5)

            if Length(midpoint-radius_vector)<radius :
                counter=counter+1
                temp_intersection=intersection_line_circle(points[temp_triangle[2]],points[temp_triangle[1]],radius,radius_vector)
                temp_angle=acos(Dot(temp_intersection[0]-radius_vector,temp_intersection[1]-radius_vector)/Length(temp_intersection[0]-radius_vector)/Length(temp_intersection[1]-radius_vector))
                volume_fraction[i]=((0.5)*radius*radius*(temp_angle-sin(temp_angle)))/area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
                counter2.append(volume_fraction[i])
            if counter>1:
                if counter2[0]>counter2[1]:
                    volume_fraction[i]=counter2[0]-counter2[1]
                else:
                    volume_fraction[i]=counter2[1]-counter2[0]
                print("poop")
        if count==1:
            temp_approximate_triangle.append(points[temp_triangle[index]])
            for k in range (3):
                if k!=index:
                    if intersection_line_circle(points[temp_triangle[index]],points[temp_triangle[k]],radius,radius_vector)[1]==-1:
                        temp_intersection=intersection_line_circle(points[temp_triangle[index]],points[temp_triangle[k]],radius,radius_vector)[0]
                        temp_approximate_triangle.append(temp_intersection)
                    else:
                        temp_intersection3=intersection_line_circle(points[temp_triangle[index]],points[temp_triangle[k]],radius,radius_vector)
                        if temp_intersection3[0].x==points[temp_triangle[index]].x and temp_intersection3[0].y==points[temp_triangle[index]].y:
                            temp_intersection=temp_intersection3[1]
                            temp_approximate_triangle.append(temp_intersection)
                        else:
                            temp_intersection=temp_intersection3[0]
                            temp_approximate_triangle.append(temp_intersection)


            temp_area=area(temp_approximate_triangle)
            temp_angle=acos(Dot(temp_approximate_triangle[1]-radius_vector,temp_approximate_triangle[2]-radius_vector)/Length(temp_approximate_triangle[2]-radius_vector)/Length(temp_approximate_triangle[1]-radius_vector))
            volume_fraction[i]=(temp_area+(0.5)*radius*radius*(temp_angle-sin(temp_angle)))/area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
            outside_points=[]
            for w in range(3):
                if w!=index:
                    outside_points.append(points[temp_triangle[w]])

            midpoint=vector((outside_points[0].x+outside_points[1].x)*0.5,(outside_points[0].y+outside_points[1].y)*0.5)
            if Length(midpoint-radius_vector)<radius:

                temp_intersection4=intersection_line_circle(outside_points[0],outside_points[1],radius,radius_vector)
                temp_angle=acos(Dot(temp_approximate_triangle[1]-radius_vector,temp_approximate_triangle[2]-radius_vector)/Length(temp_approximate_triangle[2]-radius_vector)/Length(temp_approximate_triangle[1]-radius_vector))
                temp_angle2=acos(Dot(temp_intersection4[0]-radius_vector,temp_intersection4[1]-radius_vector)/Length(temp_intersection4[0]-radius_vector)/Length(temp_intersection4[1]-radius_vector))
                volume_fraction[i]=(temp_area+(0.5)*radius*radius*(temp_angle-sin(temp_angle))-(0.5)*radius*radius*(temp_angle2-sin(temp_angle2)))/area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])

            if volume_fraction[i]>1:
                volume_fraction[i]=1
            temp_approximate_triangle=[]
        total_area[i]=volume_fraction[i]*area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
        count=0

    #triangles with two point in shape
    for i in range(len(triangles)):
        temp_triangle=triangles[i]
        index=[]
        for j in range(3):
            if (Length(points[temp_triangle[j]]-radius_vector))<=radius:
                count+=1
                index.append(j)
        if count==2:
            for p in range(3):
                if p!=index[0] and p!=index[1]:
                    index2=p
            temp_intersection2=[]
            if intersection_line_circle(points[temp_triangle[index2]],points[temp_triangle[index[0]]],radius,radius_vector)[1]==-1 and intersection_line_circle(points[temp_triangle[index2]],points[temp_triangle[index[1]]],radius,radius_vector)[1]==-1:
                for k in range(2):
                    temp_intersection2.append(intersection_line_circle(points[temp_triangle[index2]],points[temp_triangle[index[k]]],radius,radius_vector)[0])
                temp_triangle2=[temp_intersection2[0]]
                for k in range(2):
                    temp_triangle2.append(points[temp_triangle[index[k]]])
                temp_triangle3=[]
                temp_triangle3.append(temp_intersection2[0])
                temp_triangle3.append(temp_intersection2[1])
                temp_triangle3.append(points[temp_triangle[index[1]]])
                temp_area2=area(temp_triangle2)+area(temp_triangle3)
                temp_angle=acos(Dot(temp_intersection2[0]-radius_vector,temp_intersection2[1]-radius_vector)/Length(temp_intersection2[0]-radius_vector)/Length(temp_intersection2[1]-radius_vector))

                volume_fraction[i]=(temp_area2+0.5*radius*radius*(temp_angle-sin(temp_angle)))/area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
                if volume_fraction[i]>1:
                    volume_fraction[i]=1
            elif intersection_line_circle(points[temp_triangle[index2]],points[temp_triangle[index[0]]],radius,radius_vector)[1]==-1:
                temp_intersection2.append(intersection_line_circle(points[temp_triangle[index2]],points[temp_triangle[index[0]]],radius,radius_vector)[0])
                temp_intersection3=intersection_line_circle(points[temp_triangle[index2]],points[temp_triangle[index[1]]],radius,radius_vector)
                for j in range(len(temp_intersection3)):

                    if temp_intersection3[j].x!=points[temp_triangle[index[1]]].x and temp_intersection3[j].y!=points[temp_triangle[index[1]]].y:
                        temp_intersection2.append(temp_intersection3[j])

                temp_triangle2=[temp_intersection2[1]]
                for k in range(2):
                    temp_triangle2.append(points[temp_triangle[index[k]]])

                temp_triangle3=[]
                temp_triangle3.append(temp_intersection2[0])
                temp_triangle3.append(temp_intersection2[1])
                temp_triangle3.append(points[temp_triangle[index[0]]])

                temp_area2=area(temp_triangle2)+area(temp_triangle3)
                temp_angle=acos(Dot(temp_intersection2[0]-radius_vector,temp_intersection2[1]-radius_vector)/Length(temp_intersection2[0]-radius_vector)/Length(temp_intersection2[1]-radius_vector))

                volume_fraction[i]=(temp_area2+0.5*radius*radius*(temp_angle-sin(temp_angle)))/area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
                if volume_fraction[i]>1:
                    volume_fraction[i]=1
            elif intersection_line_circle(points[temp_triangle[index2]],points[temp_triangle[index[1]]],radius,radius_vector)[1]==-1:
                temp_intersection2.append(intersection_line_circle(points[temp_triangle[index2]],points[temp_triangle[index[1]]],radius,radius_vector)[0])
                temp_intersection3=intersection_line_circle(points[temp_triangle[index2]],points[temp_triangle[index[0]]],radius,radius_vector)
                for j in range(len(temp_intersection3)):
                    if temp_intersection3[j].x!=points[temp_triangle[index[0]]].x and temp_intersection3[j].y!=points[temp_triangle[index[0]]].y:
                        temp_intersection2.append(temp_intersection3[j])

                temp_triangle2=[temp_intersection2[1]]
                for k in range(2):
                    temp_triangle2.append(points[temp_triangle[index[k]]])

                temp_triangle3=[]
                temp_triangle3.append(temp_intersection2[0])
                temp_triangle3.append(temp_intersection2[1])
                temp_triangle3.append(points[temp_triangle[index[1]]])

                temp_area2=area(temp_triangle2)+area(temp_triangle3)
                temp_angle=acos(Dot(temp_intersection2[0]-radius_vector,temp_intersection2[1]-radius_vector)/Length(temp_intersection2[0]-radius_vector)/Length(temp_intersection2[1]-radius_vector))

                volume_fraction[i]=(temp_area2+0.5*radius*radius*(temp_angle-sin(temp_angle)))/area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
                if volume_fraction[i]>1:
                    volume_fraction[i]=1
        total_area[i]=volume_fraction[i]*area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
        count=0
    total=0
    for i in total_area:
        total=i+total
    print(total/pi/float((radius*radius)))
    return volume_fraction
def find_normal(points,triangles,volume_fraction,radius_vector,test):
    # Finds the normal vector
    normal_x=[]
    normal_y=[]
    for i in range(len(triangles)):
        normal_x.append(0)
        normal_y.append(0)
    for i in range(len(triangles)):
        if volume_fraction[i]!=0 and volume_fraction[i]!=1:
            triangler2=triangle(points,test.triangles()[i])
            centroid=triangler2.centroid()
            angle=atan2(centroid.y-radius_vector.y,centroid.x-radius_vector.x)
            normal_x[i]=cos(angle)
            normal_y[i]=sin(angle)

    return normal_x,normal_y
def find_adj_cell(triangles):
    # Finds the adjacent cells
    adj_cell=[]
    for i in range(len(triangles)):
        temp_adj_cell=[-1,-1,-1]
        for k in range(len(triangles)):
            if triangles[i]!=triangles[k]:
                temp_triangle=triangles[i]
                count=0
                j=[temp_triangle[0],temp_triangle[1]]
                for p in triangles[k]:
                    if p==j[0]:
                        count=count+1
                    elif p==j[1]:
                        count=count+1
                if count==2:
                    temp_adj_cell[0]=k
                count=0
                j=[temp_triangle[1],temp_triangle[2]]
                for p in triangles[k]:
                    if p==j[0]:
                        count=count+1
                    elif p==j[1]:
                        count=count+1
                if count==2:
                    temp_adj_cell[1]=k
                count=0
                j=[temp_triangle[0],temp_triangle[2]]
                for p in triangles[k]:
                    if p==j[0]:
                        count=count+1
                    elif p==j[1]:
                        count=count+1
                if count==2:
                    temp_adj_cell[2]=k
        adj_cell.append(temp_adj_cell)
    return (adj_cell)
def kernel_normalization(epsilon,test,triangles,points):
    centroid=[]
    for i in range(len(triangles)):
        triangler2=triangle(points,test.triangles()[i])
        centroid.append(triangler2.centroid())
    area_triangles=[]
    for i in triangles:
        area_triangles.append(area([points[i[0]],points[i[1]],points[i[2]]]))

    A=[]
    for x in range(len(triangles)):
        sum=0
        for i in range(len(triangles)):
            if Length(centroid[i]-centroid[x])<epsilon:
                temp=(1-(Length(centroid[i]-centroid[x])/epsilon)**2)**4*area_triangles[i]
            else:
                temp=0

            sum=sum+temp

        if sum!=0:
            A.append(1/sum)

    return(A,centroid,area_triangles)
def kernel_evaluation(A,x,x_prime,centroid):
    if Length(centroid[x_prime]-centroid[x])<epsilon:
        temp=A[x]*((1-(Length(centroid[x_prime]-centroid[x])/epsilon)**2)**4)
    else:
        temp=0
    return(temp)
def new_colour_function(centroid,area_triangles,volume_fraction,A):
    # Finds the colour function using the kernel evaluation
    new_volume_fraction=[]
    for x in range(len(volume_fraction)):
        sum=0
        for i in range(len(volume_fraction)):
            sum=sum+kernel_evaluation(A,x,i,centroid)*volume_fraction[i]*area_triangles[i]
        new_volume_fraction.append(sum)
    return(new_volume_fraction)
def find_height(volume_fraction,points,test,normal_x,normal_y,circle_center,intersection):

    #rectangle parameters
    length=11
    spacing=0.0
    approximate_radius_points_textfile=[]
    approximate_radius_points=[]
    all_rectangle_points=[]
    all_rectangle_points_height=[]
    test_height=[]
    temp_height=[]
    temp_rectangle_vertices=[]
    for w in range(len(volume_fraction)):
        temp_height=[0,0]
        approximate_radius_point=vector(-1,-1)
        approximate_radius_point2=vector(-1,-1)
        approximate_radius_point3=vector(-1,-1)
        if volume_fraction[w]!=1 and volume_fraction[w]!=0:

            normal=vector(normal_x[w],normal_y[w])
            triangler=test.triangles()
            triangler2=triangle(points,test.triangles()[w])
            centroid=triangler2.centroid()
            needed_loc=triangler[w]
            needed_points=[points[needed_loc[0]],points[needed_loc[1]],points[needed_loc[2]]]

            shifted_needed_points=[]
            temp_angle=atan2(normal_y[w],normal_x[w])
            if temp_angle<0:
                temp_angle=temp_angle+2*pi
            for p in range(3):
                temp_x=(needed_points[p].x-centroid.x)*cos(temp_angle-pi/2)+(needed_points[p].y-centroid.y)*sin(temp_angle-pi/2)
                temp_y=-(needed_points[p].x-centroid.x)*sin(temp_angle-pi/2)+(needed_points[p].y-centroid.y)*cos(temp_angle-pi/2)
                shifted_needed_points.append(vector(temp_x,temp_y))

            width=max([abs(shifted_needed_points[1].x),abs(shifted_needed_points[2].x),abs(shifted_needed_points[0].x)])*2
            width=width*2

            width=2
            #print (w)
            #for i in shifted_needed_points:
                #print(i.x)
                #print(i.y)

            if normal.x==0 and normal.y>0:
                angle=pi*0.5
            elif normal.x==0 and normal.y<0:
                angle=pi*0.5*3
            elif normal.x<0 and normal.y<0:
                angle=atan(normal.y/normal.x)+pi
            elif normal.x<0 and normal.y>0:
                angle=atan(normal.y/normal.x)+pi
            elif normal.x<0 and normal.y==0:
                angle=pi
            else:
                angle=atan(normal.y/normal.x)
            angle=angle+pi

            bottom_point=find_point_distance(centroid,angle,length*0.5)

            rectangle_vertices=find_height_function_vertices(length,width,normal,bottom_point)
            all_rectangle_points.append(rectangle_vertices)
            temp_rectangle_vertices=[rectangle_vertices[0],rectangle_vertices[1],rectangle_vertices[2],rectangle_vertices[3]]
            area_inside,area_inside2=find_area_height_function(rectangle_vertices,points,triangler,volume_fraction,intersection)

            print
            print w
            print

            height=0
            for k in range(len(volume_fraction)):
                height=height+volume_fraction[k]*area_inside2[k]
            height=height/width
            temp_height[1]=height

            #temp_rectangle_vertices[1]=find_point_distance(temp_rectangle_vertices[0],angle-pi,height)
            #temp_rectangle_vertices[2]=find_point_distance(temp_rectangle_vertices[3],angle-pi,height)
            all_rectangle_points_height.append(temp_rectangle_vertices)
            appr_circl=find_point_distance(bottom_point,angle-pi,height)
            approximate_radius_point=appr_circl



            bottom_point2=find_point_distance(bottom_point,angle-pi/2,width+spacing)
            rectangle_vertices=find_height_function_vertices(length,width,normal,bottom_point2)
            all_rectangle_points.append(rectangle_vertices)
            temp_rectangle_vertices=[rectangle_vertices[0],rectangle_vertices[1],rectangle_vertices[2],rectangle_vertices[3]]
            area_inside,area_inside2=find_area_height_function(rectangle_vertices,points,triangler,volume_fraction,intersection)


            print

            height=0
            for k in range(len(volume_fraction)):
                height=height+volume_fraction[k]*area_inside2[k]
            height=height/width
            temp_height[0]=height
            #temp_rectangle_vertices[1]=find_point_distance(temp_rectangle_vertices[0],angle-pi,height)
            #temp_rectangle_vertices[2]=find_point_distance(temp_rectangle_vertices[3],angle-pi,height)
            all_rectangle_points_height.append(temp_rectangle_vertices)
            appr_circl=find_point_distance(bottom_point2,angle-pi,height)
            approximate_radius_point2=appr_circl





            bottom_point3=find_point_distance(bottom_point,angle+pi/2,width+spacing)
            rectangle_vertices=find_height_function_vertices(length,width,normal,bottom_point3)
            all_rectangle_points.append(rectangle_vertices)
            temp_rectangle_vertices=[rectangle_vertices[0],rectangle_vertices[1],rectangle_vertices[2],rectangle_vertices[3]]
            area_inside,area_inside2=find_area_height_function(rectangle_vertices,points,triangler,volume_fraction,intersection)

            print
            height=0
            for k in range(len(volume_fraction)):
                height=height+volume_fraction[k]*area_inside2[k]
            height=height/width

            #temp_rectangle_vertices[1]=find_point_distance(temp_rectangle_vertices[0],angle-pi,height)
            #temp_rectangle_vertices[2]=find_point_distance(temp_rectangle_vertices[3],angle-pi,height)
            all_rectangle_points_height.append(temp_rectangle_vertices)
            appr_circl=find_point_distance(bottom_point3,angle-pi,height)
            approximate_radius_point3=appr_circl


        test_height.append(abs(temp_height[0]-temp_height[1]))
        approximate_radius_points.append([approximate_radius_point,approximate_radius_point2,approximate_radius_point3])

        if approximate_radius_point.x!=-1 and approximate_radius_point.y!=-1:
            approximate_radius_points_textfile.append(approximate_radius_point)
            approximate_radius_points_textfile.append(approximate_radius_point2)
            approximate_radius_points_textfile.append(approximate_radius_point3)






    #print(area_inside)
    temp_max=0
    max_index=0
    print(test_height)
    for j in range(len(test_height)):
        if temp_max<test_height[j]:
            temp_max=test_height[j]
            max_index=j
    print(max_index)
    print(test_height[max_index])
    return approximate_radius_points,all_rectangle_points_height
def find_point_distance(point,angle,distance):
    # Finds the point a specific distance and angle away from a point
    return vector(cos(angle)*distance+point.x,sin(angle)*distance+point.y)
def find_height_function_vertices(length,width,normal_vector,bottom_point):
    # finds the height function vertices
    #finding rectangle vertices
    rectangle_vertices=[]
    if normal_vector.y>0 and normal_vector.x==0:
        rectangle_vertices.append(vector(bottom_point.x-width*0.5,bottom_point.y))
        rectangle_vertices.append(vector(bottom_point.x-width*0.5,bottom_point.y+length))
        rectangle_vertices.append(vector(bottom_point.x+width*0.5,bottom_point.y+length))
        rectangle_vertices.append(vector(bottom_point.x+width*0.5,bottom_point.y))
    elif normal_vector.y<0 and normal_vector.x==0:
        rectangle_vertices.append(vector(bottom_point.x+width*0.5,bottom_point.y))
        rectangle_vertices.append(vector(bottom_point.x+width*0.5,bottom_point.y-length))
        rectangle_vertices.append(vector(bottom_point.x-width*0.5,bottom_point.y-length))
        rectangle_vertices.append(vector(bottom_point.x-width*0.5,bottom_point.y))
    elif normal_vector.x>0 and normal_vector.y==0:
        rectangle_vertices.append(vector(bottom_point.x,bottom_point.y+width*0.5))
        rectangle_vertices.append(vector(bottom_point.x+length,bottom_point.y+width*0.5))
        rectangle_vertices.append(vector(bottom_point.x+length,bottom_point.y-width*0.5))
        rectangle_vertices.append(vector(bottom_point.x,bottom_point.y-width*0.5))
    elif normal_vector.x<0 and normal_vector.y==0:
        rectangle_vertices.append(vector(bottom_point.x,bottom_point.y-width*0.5))
        rectangle_vertices.append(vector(bottom_point.x-length,bottom_point.y-width*0.5))
        rectangle_vertices.append(vector(bottom_point.x-length,bottom_point.y+width*0.5))
        rectangle_vertices.append(vector(bottom_point.x,bottom_point.y+width*0.5))
    elif normal_vector.x>0 and normal_vector.y>0:
        rectangle_vertices.append(find_point_distance(bottom_point,pi*0.5+atan(normal_vector.y/normal_vector.x),width*0.5))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[0],atan(normal_vector.y/normal_vector.x),length))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[1],-pi*0.5+atan(normal_vector.y/normal_vector.x),width))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[2],pi+atan(normal_vector.y/normal_vector.x),length))
    elif normal_vector.x<0 and normal_vector.y>0:
        rectangle_vertices.append(find_point_distance(bottom_point,3*0.5*pi-atan(-normal_vector.y/normal_vector.x),width*0.5))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[0],pi-atan(-normal_vector.y/normal_vector.x),length))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[1],pi*0.5-atan(-normal_vector.y/normal_vector.x),width))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[2],-atan(-normal_vector.y/normal_vector.x),length))
    elif normal_vector.x<0 and normal_vector.y<0:
        rectangle_vertices.append(find_point_distance(bottom_point,pi*3*0.5+atan(normal_vector.y/normal_vector.x),width*0.5))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[0],pi+atan(normal_vector.y/normal_vector.x),length))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[1],pi*0.5+atan(normal_vector.y/normal_vector.x),width))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[2],atan(normal_vector.y/normal_vector.x),length))
    elif normal_vector.x>0 and normal_vector.y<0:
        rectangle_vertices.append(find_point_distance(bottom_point,pi*3*0.5-atan(-normal_vector.y/normal_vector.x),width*0.5))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[0],-atan(-normal_vector.y/normal_vector.x),length))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[1],pi*0.5-atan(-normal_vector.y/normal_vector.x),width))
        rectangle_vertices.append(find_point_distance(rectangle_vertices[2],pi-atan(-normal_vector.y/normal_vector.x),length))
    return rectangle_vertices
def find_area_height_function(rectangle_vertices,points,triangles,volume_fraction,intersection):

    # Finds the area of height function
    rectangle_vertices.append(rectangle_vertices[0])
    list_of_inside_triangles=[]
    area_inside_rectangle=[]

    for i in range(len(triangles)):
        area_inside_rectangle.append(0)

    for i in range(len(triangles)):

        required_points=[]
        i2=triangles[i]
        i2.append(i2[0])
        temp_intersection=[]
        for j in range(len(rectangle_vertices)-1):
            for k in range(len(i2)-1):
                if intersection_line_line(points[i2[k]],points[i2[k+1]],rectangle_vertices[j],rectangle_vertices[j+1])!=False:
                    list_of_inside_triangles.append(i2)
                    temp_intersection.append(intersection_line_line(points[i2[k]],points[i2[k+1]],rectangle_vertices[j],rectangle_vertices[j+1]))
                    required_points.append(intersection_line_line(points[i2[k]],points[i2[k+1]],rectangle_vertices[j],rectangle_vertices[j+1]))

        temp=[]
        temp_triangle=triangles[i]

        for j in range(len(temp_triangle)-1):
            if (0<Dot(points[temp_triangle[j]]-rectangle_vertices[1],rectangle_vertices[2]-rectangle_vertices[1])<Dot(rectangle_vertices[2]-rectangle_vertices[1],rectangle_vertices[2]-rectangle_vertices[1])) and (0<Dot(points[temp_triangle[j]]-rectangle_vertices[1],rectangle_vertices[0]-rectangle_vertices[1])<Dot(rectangle_vertices[0]-rectangle_vertices[1],rectangle_vertices[0]-rectangle_vertices[1])):
                temp.append(points[temp_triangle[j]])
                required_points.append(points[temp_triangle[j]])
        rec=[]
        for j in range(len(rectangle_vertices)-1):
                total_area=area([points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]])
                area1=area([rectangle_vertices[j],points[temp_triangle[1]],points[temp_triangle[2]]])
                area2=area([rectangle_vertices[j],points[temp_triangle[0]],points[temp_triangle[2]]])
                area3=area([rectangle_vertices[j],points[temp_triangle[0]],points[temp_triangle[1]]])
                if abs(area1+area2+area3-total_area)<0.000001:
                    rec.append(rectangle_vertices[j])
                    required_points.append(rectangle_vertices[j])
        for j in range(len(rectangle_vertices)-1):
            for k in range(len(temp_triangle)-1):
                if abs(Length(rectangle_vertices[j]-points[temp_triangle[k]])+Length(rectangle_vertices[j]-points[temp_triangle[k+1]])-Length(points[temp_triangle[k+1]]-points[temp_triangle[k]]))<0.00000001:
                    required_points.append(rectangle_vertices[j])

        distance=0
        index=-1
        for j in range(len(required_points)):
            if required_points[j].x>distance:
                distance=required_points[j].x
                index=j
        if index!=-1:

            required_points_sorted=sort_counterclockwise(required_points[index],required_points)

            area_inside_rectangle[i]=area_polygon(required_points_sorted[0],required_points_sorted)


    total=0
    for i in area_inside_rectangle:
        total=total+i

    print (total)

    area_inside_rectangle2=[]
    for i in area_inside_rectangle:
        area_inside_rectangle2.append(i)
    #list_of_inside_triangles=[]
    for i in range(len(triangles)):
        if volume_fraction[i]!=0 and volume_fraction[i]!=1:
            if area_inside_rectangle[i]> 0:

                if len(intersection[i])==4:
                    required_points=[]
                    ttemp=intersection[i]

                    i2=[ttemp[1],ttemp[2],ttemp[3]]
                    i2.append(i2[0])
                    temp_intersection=[]
                    for j in range(len(rectangle_vertices)-1):
                        for k in range(len(i2)-1):
                            if intersection_line_line(i2[k],i2[k+1],rectangle_vertices[j],rectangle_vertices[j+1])!=False:
                                list_of_inside_triangles.append(i2)
                                temp_intersection.append(intersection_line_line(i2[k],i2[k+1],rectangle_vertices[j],rectangle_vertices[j+1]))
                                required_points.append(intersection_line_line(i2[k],i2[k+1],rectangle_vertices[j],rectangle_vertices[j+1]))

                    temp=[]
                    temp_triangle=[ttemp[1],ttemp[2],ttemp[3],ttemp[1]]

                    for j in range(len(temp_triangle)-1):
                        if (0<Dot(temp_triangle[j]-rectangle_vertices[1],rectangle_vertices[2]-rectangle_vertices[1])<Dot(rectangle_vertices[2]-rectangle_vertices[1],rectangle_vertices[2]-rectangle_vertices[1])) and (0<Dot(temp_triangle[j]-rectangle_vertices[1],rectangle_vertices[0]-rectangle_vertices[1])<Dot(rectangle_vertices[0]-rectangle_vertices[1],rectangle_vertices[0]-rectangle_vertices[1])):
                            temp.append(temp_triangle[j])
                            required_points.append(temp_triangle[j])
                    rec=[]
                    for j in range(len(rectangle_vertices)-1):
                            total_area=area([temp_triangle[0],temp_triangle[1],temp_triangle[2]])
                            area1=area([rectangle_vertices[j],temp_triangle[1],temp_triangle[2]])
                            area2=area([rectangle_vertices[j],temp_triangle[0],temp_triangle[2]])
                            area3=area([rectangle_vertices[j],temp_triangle[0],temp_triangle[1]])
                            if abs(area1+area2+area3-total_area)<0.000001:
                                rec.append(rectangle_vertices[j])
                                required_points.append(rectangle_vertices[j])
                    for j in range(len(rectangle_vertices)-1):
                        for k in range(len(temp_triangle)-1):
                            if abs(Length(rectangle_vertices[j]-temp_triangle[k])+Length(rectangle_vertices[j]-temp_triangle[k+1])-Length(temp_triangle[k+1]-temp_triangle[k]))<0.00000001:
                                required_points.append(rectangle_vertices[j])

                    distance=0
                    index=-1
                    for j in range(len(required_points)):
                        if required_points[j].x>distance:
                            distance=required_points[j].x
                            index=j
                    if index!=-1:

                        required_points_sorted=sort_counterclockwise(required_points[index],required_points)
                        '''
                        print "area is:"
                        print ttemp[1].x
                        print ttemp[1].y
                        print area([ttemp[1],ttemp[2],ttemp[3]])
                        print area_polygon(required_points_sorted[0],required_points_sorted)
                        print area_inside_rectangle[i]
                        '''
                        area_inside_rectangle2[i]=(area_inside_rectangle[i]-area_polygon(required_points_sorted[0],required_points_sorted))/volume_fraction[i]
                if len(intersection[i])==3:
                    required_points=[]
                    ttemp=intersection[i]

                    i2=[ttemp[0],ttemp[1],ttemp[2]]
                    i2.append(i2[0])
                    temp_intersection=[]
                    for j in range(len(rectangle_vertices)-1):
                        for k in range(len(i2)-1):
                            if intersection_line_line(i2[k],i2[k+1],rectangle_vertices[j],rectangle_vertices[j+1])!=False:
                                list_of_inside_triangles.append(i2)
                                temp_intersection.append(intersection_line_line(i2[k],i2[k+1],rectangle_vertices[j],rectangle_vertices[j+1]))
                                required_points.append(intersection_line_line(i2[k],i2[k+1],rectangle_vertices[j],rectangle_vertices[j+1]))

                    temp=[]
                    temp_triangle=[ttemp[0],ttemp[1],ttemp[2],ttemp[1]]

                    for j in range(len(temp_triangle)-1):
                        if (0<Dot(temp_triangle[j]-rectangle_vertices[1],rectangle_vertices[2]-rectangle_vertices[1])<Dot(rectangle_vertices[2]-rectangle_vertices[1],rectangle_vertices[2]-rectangle_vertices[1])) and (0<Dot(temp_triangle[j]-rectangle_vertices[1],rectangle_vertices[0]-rectangle_vertices[1])<Dot(rectangle_vertices[0]-rectangle_vertices[1],rectangle_vertices[0]-rectangle_vertices[1])):
                            temp.append(temp_triangle[j])
                            required_points.append(temp_triangle[j])
                    rec=[]
                    for j in range(len(rectangle_vertices)-1):
                            total_area=area([temp_triangle[0],temp_triangle[1],temp_triangle[2]])
                            area1=area([rectangle_vertices[j],temp_triangle[1],temp_triangle[2]])
                            area2=area([rectangle_vertices[j],temp_triangle[0],temp_triangle[2]])
                            area3=area([rectangle_vertices[j],temp_triangle[0],temp_triangle[1]])
                            if abs(area1+area2+area3-total_area)<0.000001:
                                rec.append(rectangle_vertices[j])
                                required_points.append(rectangle_vertices[j])
                    for j in range(len(rectangle_vertices)-1):
                        for k in range(len(temp_triangle)-1):
                            if abs(Length(rectangle_vertices[j]-temp_triangle[k])+Length(rectangle_vertices[j]-temp_triangle[k+1])-Length(temp_triangle[k+1]-temp_triangle[k]))<0.00000001:
                                required_points.append(rectangle_vertices[j])

                    distance=0
                    index=-1
                    for j in range(len(required_points)):
                        if required_points[j].x>distance:
                            distance=required_points[j].x
                            index=j
                    if index!=-1:

                        required_points_sorted=sort_counterclockwise(required_points[index],required_points)
                        '''
                        print "area is:"
                        print ttemp[1].x
                        print ttemp[1].y
                        print area([ttemp[0],ttemp[1],ttemp[2]])
                        print area_polygon(required_points_sorted[0],required_points_sorted)
                        print area_inside_rectangle[i]
                        '''
                        area_inside_rectangle2[i]=area_polygon(required_points_sorted[0],required_points_sorted)/volume_fraction[i]


    return (area_inside_rectangle,area_inside_rectangle2)
def celeste(volume_fraction,adj_cell,points,triangles,radius,test,new_volume_fraction):
    centroid=[]
    for i in range(len(triangles)):
        triangler2=triangle(points,test.triangles()[i])
        centroid.append(triangler2.centroid())

    normal=[]
    for i in range(len(new_volume_fraction)):
        temp_adj_cell=adj_cell[i]
        if temp_adj_cell[0]!=-1 and temp_adj_cell[1]!=-1 and temp_adj_cell[2]!=-1:

            temp_centroid=centroid[i]
            b=np.array([[(new_volume_fraction[temp_adj_cell[0]]-new_volume_fraction[i])/Length(temp_centroid-centroid[temp_adj_cell[0]])**2],[(new_volume_fraction[temp_adj_cell[1]]-new_volume_fraction[i])/Length(temp_centroid-centroid[temp_adj_cell[1]])**2],[(new_volume_fraction[temp_adj_cell[2]]-new_volume_fraction[i])/Length(temp_centroid-centroid[temp_adj_cell[2]])**2]])
            A=np.empty((0,5))

            for j in range(3):
                temp=np.array([[centroid[temp_adj_cell[j]].x-temp_centroid.x,centroid[temp_adj_cell[j]].y-temp_centroid.y,(centroid[temp_adj_cell[j]].x-temp_centroid.x)**2*0.5,(centroid[temp_adj_cell[j]].y-temp_centroid.y)**2*0.5,(centroid[temp_adj_cell[j]].x-temp_centroid.x)*(centroid[temp_adj_cell[j]].y-temp_centroid.y)]])
                temp=temp/(Length(centroid[temp_adj_cell[j]]-temp_centroid)**2)
                A=np.vstack((A,temp))
            round1=11


            x=np.linalg.lstsq(A,b)[0]



            if Length(vector(x[0],x[1]))==0:
                temp_normal=vector(0,0)
            else:
                temp_normal=vector(x[0],x[1])*(1/Length(vector(x[0],x[1])))

            normal.append(temp_normal)

        else:
            normal.append(vector(0,0))


    curvature=[]
    for i in range(len(volume_fraction)):
        temp_adj_cell=adj_cell[i]
        if not Length(normal[i])==0:
            temp_centroid=centroid[i]
            b=np.array([[(normal[temp_adj_cell[0]].x-normal[i].x)],[(normal[temp_adj_cell[1]].x-normal[i].x)],[(normal[temp_adj_cell[2]].x-normal[i].x)]])
            A=np.empty((0,3))
            for j in range(3):
                temp=np.array([[centroid[temp_adj_cell[j]].x-temp_centroid.x,centroid[temp_adj_cell[j]].y-temp_centroid.y,0]])
                A=np.vstack((A,temp))

            x=np.linalg.lstsq(A,b)[0]

            del_x=x[0][0]

            b=np.array([[(normal[temp_adj_cell[0]].y-normal[i].y)],[(normal[temp_adj_cell[1]].y-normal[i].y)],[(normal[temp_adj_cell[2]].y-normal[i].y)]])

            y=np.linalg.lstsq(A,b)[0]

            del_y=y[1][0]


            b=np.array([[(0)],[(0)],[(0)]])
            z=np.linalg.lstsq(A,b)[0]
            del_z=z[2][0]

            curvature.append(-(del_x+del_y+del_z))

        else:
            curvature.append([])

    #print(len(curvature))

    return normal,curvature,centroid
def curvature(volume_fraction,approximate_radius_points,test,points,radius,normal_x,normal_y,circle_center):
    parabolic_approximation_coefficients=[]
    singular_matrix_index=[]

    shifted_approximate_radius_points=[]

    list_centroid=[]

    for w in range(len(volume_fraction)):
        triangler2=triangle(points,test.triangles()[w])
        list_centroid.append(triangler2.centroid())
    print(singular_matrix_index)

    for i in range(len(volume_fraction)):
        temp_shifted_approximate_radius_points=[]
        if volume_fraction[i]!=0 and volume_fraction[i]!=1:
            j=approximate_radius_points[i]
            temp_angle=(atan2(normal_y[i],normal_x[i]))
            if temp_angle<0:
                temp_angle=temp_angle+2*pi
            temp_shifted_approximate_radius_points=[]
            for w in range(3):
                temp_x=(j[w].x-j[0].x)*cos(temp_angle-pi/2)+(j[w].y-j[0].y)*sin(temp_angle-pi/2)
                temp_y=-(j[w].x-j[0].x)*sin(temp_angle-pi/2)+(j[w].y-j[0].y)*cos(temp_angle-pi/2)


                temp_shifted_approximate_radius_points.append(vector(temp_x,temp_y))

        shifted_approximate_radius_points.append(temp_shifted_approximate_radius_points)






    for k in range(len(approximate_radius_points)):
        j=shifted_approximate_radius_points[k]
        x=np.matrix([[0]])
        if j!=[] :
            a=np.array([[j[0].x**2,j[0].x,1],[j[1].x**2,j[1].x,1],[j[2].x**2,j[2].x,1]])
            if np.linalg.det(a)!=0:
                b=np.array([[j[0].y],[j[1].y],[j[2].y]])
                x=np.linalg.solve(a,b)
            else:
                a=np.array([[j[0].y**2,j[0].y,1],[j[1].y**2,j[1].y,1],[j[2].y**2,j[2].y,1]])
                b=np.array([[j[0].x],[j[1].x],[j[2].x]])
                x=np.linalg.solve(a,b)
                singular_matrix_index.append(k)
                print("singular matrix")
        parabolic_approximation_coefficients.append(x)


    curvature=[]
    curvature2=[]
    for w in range(len(list_centroid)):
        temp_parabolic_approximation_coefficients=parabolic_approximation_coefficients[w]
        if len(temp_parabolic_approximation_coefficients)!=1:
            if w not in singular_matrix_index:
                curvature.append(2*temp_parabolic_approximation_coefficients[0][0]/(1+(temp_parabolic_approximation_coefficients[1][0])**2)**(1.5))
                curvature2.append(2*temp_parabolic_approximation_coefficients[0][0]/(1+(temp_parabolic_approximation_coefficients[1][0])**2)**(1.5))
        else:
            curvature2.append(abs(1/float(radius)))
    error_curvature_max=[]
    print "start"
    print(len(curvature))

    for w in curvature:
        error_curvature_max.append(abs(1/float(radius)-abs(w)))
    print(curvature)
    print(error_curvature_max)

    print(max(error_curvature_max)/abs(1/float(radius)))


    print(np.linalg.norm((error_curvature_max),ord=2)/float(len(curvature))**0.5/abs(1/float(radius)))



    error_curvature_max1=[]
    print(len(curvature))

    for w in curvature2:
        error_curvature_max1.append(abs(1/float(radius)-abs(w)))

    print(error_curvature_max1)

    max1=0
    count=1
    max_index=0
    for j in range(len(curvature2)):
        if error_curvature_max1[j]!=0:
            count=count+1
        if abs(error_curvature_max1[j])>max1:
            max1=abs(error_curvature_max1[j])
            max_index=j
            max_count=count

    print(max_index)
    print(max1)
    print(max_count)




    return (list_centroid,curvature,error_curvature_max)
def round_curvature(normal,curvature,volume_fraction,adj_cell,centroid,radius):


    weighting_factor=[]
    for i in range(len(volume_fraction)):
        weighting_factor.append((1-2*(abs(0.5-volume_fraction[i])))**8)

    curvature2=[]
    for i in range(len(volume_fraction)):
        if not Length(normal[i])==0:
            temp_adj_cell=adj_cell[i]
            numerator=curvature[i]*weighting_factor[i]
            denominator=weighting_factor[i]

            for j in temp_adj_cell:
                if weighting_factor[j]!=0:
                    numerator=numerator+curvature[j]*weighting_factor[j]
                    denominator=denominator+weighting_factor[j]
            if denominator==0:
                curvature2.append([])
            else:
                curvature2.append(numerator/denominator)
        else:
            curvature2.append([])


    weighting_factor2=[]
    s_q=[]
    for i in range(len(volume_fraction)):
        temp_s_q=[]
        if not Length(normal[i])==0:
            temp_adj_cell=adj_cell[i]

            for j in temp_adj_cell:
                temp_s_q.append((centroid[i]-centroid[j])*(1/Length(centroid[i]-centroid[j])))

        s_q.append(temp_s_q)



    for i in range(len(volume_fraction)):
        temp_weighting_factor2=[]
        if not Length(normal[i])==0:
            temp_s_q=s_q[i]
            temp_adj_cell=adj_cell[i]
            for j in range(len(temp_adj_cell)):
                temp_weighting_factor2.append(abs(Dot(normal[i],temp_s_q[j]))**8)
        weighting_factor2.append(temp_weighting_factor2)





    curvature3=[]
    for i in range(len(volume_fraction)):
        if not Length(normal[i])==0 and not curvature2[i]==[]:
            temp_adj_cell=adj_cell[i]
            temp_weighting_factor2=weighting_factor2[i]
            numerator=curvature2[i]*weighting_factor[i]
            denominator=weighting_factor[i]
            count=0
            for j in temp_adj_cell:
                if weighting_factor[j]!=0:
                    numerator=numerator+curvature2[j]*weighting_factor[j]*temp_weighting_factor2[count]
                    denominator=denominator+weighting_factor[j]*temp_weighting_factor2[count]
                count=count+1
            if denominator==0:
                curvature3.append([])
            else:
                curvature3.append(numerator/denominator)
        else:
            curvature3.append([])

    curvature4=[]
    for i in range(len(curvature3)):
        if not curvature3[i]==[]:
            if volume_fraction[i]!=0 and volume_fraction[i]!=1:
                curvature4.append(curvature3[i])


    print(len(curvature4))
    error_curvature_max=[]


    for w in range(len(curvature4)):
        error_curvature_max.append(abs(1/float(radius)-abs(curvature4[w])))

    print(error_curvature_max)

    print(max(error_curvature_max))
    print(max(error_curvature_max)/abs(1/float(radius)))

    print(np.linalg.norm((error_curvature_max),ord=2)/(float(len(curvature4))**0.5)/abs(1/float(radius)))
    print





    error_curvature_max=[]
def plic(points,triangles,volume_fraction,normal_x,normal_y,circle_center):
    # PLIC reconstruction
    intersection=[]

    for w in range(len(triangles)):
        temp_all_intersect=[]
        if volume_fraction[w]!=0 and volume_fraction[w]!=1:

            temp_triangle=triangles[w]
            temp_points=[points[temp_triangle[0]],points[temp_triangle[1]],points[temp_triangle[2]]]
            distance=1000
            index=vector(0,0)
            for j in range(3):
                if distance>Length(temp_points[j]-circle_center):
                    distance=Length(temp_points[j]-circle_center)
                    index=temp_points[j]

            normal=vector(normal_x[w],normal_y[w])


            shifted_needed_points=[]
            temp_angle=atan2(normal_y[w],normal_x[w])
            if temp_angle<0:
                temp_angle=temp_angle+2*pi
            for p in range(3):
                temp_x=(temp_points[p].x-index.x)*cos(temp_angle-pi/2)+(temp_points[p].y-index.y)*sin(temp_angle-pi/2)
                temp_y=-(temp_points[p].x-index.x)*sin(temp_angle-pi/2)+(temp_points[p].y-index.y)*cos(temp_angle-pi/2)
                shifted_needed_points.append(vector(temp_x,temp_y))


            index2=vector(0,0)
            distance=1000
            for j in range(3):
                if distance>abs(shifted_needed_points[j].y) and index!=temp_points[j]:
                    distance=abs(shifted_needed_points[j].y)
                    index2=shifted_needed_points[j]
            for j in range(3):
                if index2!=shifted_needed_points[j] and Length(vector(0.0,0.0)-shifted_needed_points[j])>0.0000001:
                    index3=shifted_needed_points[j]
            temp_intersect=intersection_line_line(vector(100,index2.y),vector(-100,index2.y),vector(0,0),index3)

            temp_fraction=area([vector(0,0),index2,temp_intersect])/area([vector(0,0),index2,index3])


            if temp_fraction<volume_fraction[w]:

                if abs(index2.y-index3.y)<0.00000001:
                    print "poop"
                    above=index2.y
                    below=0
                else:
                    above=index3.y
                    below=index2.y
                while True:
                    if temp_fraction-volume_fraction[w]<-0.000001:

                        tall=(above+below)/2.0
                        temp_intersect1=intersection_line_line(vector(100,tall),vector(-100,tall),index2,index3)
                        temp_intersect2=intersection_line_line(vector(100,tall),vector(-100,tall),vector(0,0),index3)
                        a=sort_counterclockwise(vector(0,0),[vector(0,0),index2,temp_intersect1,temp_intersect2])
                        temp_fraction=area_polygon(a[0],a)/area([vector(0,0),index2,index3])
                        if temp_fraction-volume_fraction[w]<-0.000001:
                            below=tall
                        elif temp_fraction-volume_fraction[w]>0.000001:
                            above=tall
                    elif temp_fraction-volume_fraction[w]>0.000001:
                        tall=(below+above)/2.0
                        temp_intersect1=intersection_line_line(vector(100,tall),vector(-100,tall),index2,index3)
                        temp_intersect2=intersection_line_line(vector(100,tall),vector(-100,tall),vector(0,0),index3)
                        a=sort_counterclockwise(vector(0,0),[vector(0,0),index2,temp_intersect1,temp_intersect2])
                        temp_fraction=area_polygon(a[0],a)/area([vector(0,0),index2,index3])
                        if temp_fraction-volume_fraction[w]<-0.000001:
                            below=tall
                        elif temp_fraction-volume_fraction[w]>0.000001:
                            above=tall
                    else:

                        temp_all_intersect.append(index)
                        temp_x=(index3.x)*cos(-temp_angle+pi/2)+(index3.y)*sin(-temp_angle+pi/2)+index.x
                        temp_y=-(index3.x)*sin(-temp_angle+pi/2)+(index3.y)*cos(-temp_angle+pi/2)+index.y
                        temp_all_intersect.append(vector(temp_x,temp_y))
                        temp_x=(temp_intersect1.x)*cos(-temp_angle+pi/2)+(temp_intersect1.y)*sin(-temp_angle+pi/2)+index.x
                        temp_y=-(temp_intersect1.x)*sin(-temp_angle+pi/2)+(temp_intersect1.y)*cos(-temp_angle+pi/2)+index.y
                        temp_all_intersect.append(vector(temp_x,temp_y))

                        temp_x=(temp_intersect2.x)*cos(-temp_angle+pi/2)+(temp_intersect2.y)*sin(-temp_angle+pi/2)+index.x
                        temp_y=-(temp_intersect2.x)*sin(-temp_angle+pi/2)+(temp_intersect2.y)*cos(-temp_angle+pi/2)+index.y
                        temp_all_intersect.append(vector(temp_x,temp_y))
                        break



            elif temp_fraction>volume_fraction[w]:

                above=index2.y
                below=0
                while True:

                    tall=(below+above)/2.0
                    temp_intersect2=intersection_line_line(vector(100,tall),vector(-100,tall),vector(0,0),index3)
                    temp_intersect1=intersection_line_line(vector(100,tall),vector(-100,tall),index2,vector(0,0))
                    temp_fraction=area([vector(0,0),temp_intersect2,temp_intersect1])/area([vector(0,0),index2,index3])
                    if temp_fraction-volume_fraction[w]<-0.000001:
                        below=tall
                    elif temp_fraction-volume_fraction[w]>0.000001:
                        above=tall
                    else:

                        temp_all_intersect.append(index)
                        temp_x=(temp_intersect1.x)*cos(-temp_angle+pi/2)+(temp_intersect1.y)*sin(-temp_angle+pi/2)+index.x
                        temp_y=-(temp_intersect1.x)*sin(-temp_angle+pi/2)+(temp_intersect1.y)*cos(-temp_angle+pi/2)+index.y
                        temp_all_intersect.append(vector(temp_x,temp_y))
                        temp_x=(temp_intersect2.x)*cos(-temp_angle+pi/2)+(temp_intersect2.y)*sin(-temp_angle+pi/2)+index.x
                        temp_y=-(temp_intersect2.x)*sin(-temp_angle+pi/2)+(temp_intersect2.y)*cos(-temp_angle+pi/2)+index.y
                        temp_all_intersect.append(vector(temp_x,temp_y))


                        break
        intersection.append(temp_all_intersect)

    return intersection
#mesh parameters
#l=2 #length of triangle
#h=30 #number of rows
#n=30 #number of columns
#circle parameters
radius=9 #radius of circle
circle_center=find_center_of_circle()
#kernel parameter
epsilon=5



points=create_points()
test=unstructured_mesh(points)
triangler=test.triangles()
volume_fraction=find_volume_fraction(points,triangler,radius,circle_center)
adj_cell=find_adj_cell(triangler)
### analytical



normal_x,normal_y=find_normal(points,triangler,volume_fraction,circle_center,test)
intersection=plic(points,triangler,volume_fraction,normal_x,normal_y,circle_center)


approximate_radius_points,all_rectangle_points=find_height(volume_fraction,points,test,normal_x,normal_y,circle_center,intersection)
list_centroid,curvature_height,error_curvature=curvature(volume_fraction,approximate_radius_points,test,points,radius,normal_x,normal_y,circle_center)
###least-squares
'''
A,centroid,area_triangles=kernel_normalization(epsilon,test,triangler,points)
new_volume_fraction=new_colour_function(centroid,area_triangles,volume_fraction,A)
normal_least_squares,curvature_least_squares,centroid=celeste(volume_fraction,adj_cell,points,triangler,radius,test,new_volume_fraction)
round_curvature(normal_least_squares,curvature_least_squares,volume_fraction,adj_cell,centroid,radius)
'''
###least-squares+height
'''
normal_x=[]
normal_y=[]
for i in normal_least_squares:
    normal_x.append(-i.x)
    normal_y.append(-i.y)

approximate_radius_points,all_rectangle_points,all_height=find_height(volume_fraction,points,test,normal_x,normal_y,circle_center)
list_centroid,curvature_height,error_curvature=curvature(volume_fraction,approximate_radius_points,test,points,radius,normal_x,normal_y,circle_center,all_height)
'''
create_text(points,triangler,volume_fraction,normal_x,normal_y,all_rectangle_points,error_curvature,curvature_height,volume_fraction)