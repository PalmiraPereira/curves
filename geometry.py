from math import sqrt, pi

def dot(u, v):
    return u.x*v.x + u.y*v.y

def cross(u, v):
    return u.x*v.y - u.y*v.x

class Vector2D(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def mag(self):
        return sqrt(self.x**2 + self.y**2)

    def unit(self):
        return Vector2D(self.x, self.y)/self.mag()

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __rmul__(self, other):
        return Vector2D(other*self.x, other*self.y)

    def __div__(self, other):
        return Vector2D(self.x/other, self.y/other)

    def __str__(self):
        return '({},{})'.format(self.x, self.y)

class Line2D(object):
    def __init__(self, r0=Vector2D(), d=Vector2D()):
        self.r0 = r0
        self.d = d.unit()

    def intersect(self, other):
        dr0 = other.r0 - self.r0
        t1, t2 = cross(dr0, -other.d)/cross(self.d, -other.d), cross(self.d, dr0)/cross(self.d, -other.d)

        return self(t1)

    def __call__(self, t):
        return self.r0 + t*self.d

class LineSegment2D(object):
    def __init__(self, pt_a=Vector2D(), pt_b=Vector2D()):
        self.pt_a = pt_a
        self.pt_b = pt_b

    def projection_is_bounded(self, pt):
        t = dot(pt - self.pt_a, (self.pt_b - self.pt_a).unit())
        return t >= 0. and t <= (self.pt_b - self.pt_a).mag()

    def intersection(self, other):
        if isinstance(other, Line2D):
            xc = other.intersect(Line2D(self.pt_a, self.pt_b - self.pt_a))
            return xc if self.projection_is_bounded(xc) else None
        elif isinstance(other, LineSegment2D):
            xc = Line2D(self.pt_a, self.pt_b - self.pt_a).intersect(Line2D(other.pt_a, other.pt_b - other.pt_a))
            return xc if self.projection_is_bounded(xc) and other.projection_is_bounded(xc) else None

class Triangle(object):
    def __init__(self, verts):
        self.verts = [vert for vert in verts]

    def area(self):
        return abs(cross(self.verts[1] - self.verts[0], self.verts[2] - self.verts[0]))/2.

    def centroid(self):
        return (self.verts[0] + self.verts[1] + self.verts[2])/3.

class Circle(object):
    def __init__(self, center=Vector2D(0., 0.), radius=0.):
        self.center = center
        self.radius = radius

    def area(self):
        return pi*self.radius**2

if __name__ == '__main__':
    verts = Vector2D(0, 0), Vector2D(0, 1), Vector2D(1, 1)

    tri = Triangle(verts)
    print tri.centroid(), tri.area()

    l1 = Line2D(Vector2D(0, 0), Vector2D(0, 1))
    l2 = Line2D(Vector2D(1, 0), Vector2D(-1, 1))

    print l1.intersect(l2)
    print l2.intersect(l1)

    l1 = LineSegment2D(Vector2D(0, 0), Vector2D(0, 1))
    l2 = LineSegment2D(Vector2D(1, 0), Vector2D(0.432, 0.89))

    print l1.intersection(l2)
    print l2.intersection(l1)
