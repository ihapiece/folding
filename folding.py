from math import *

class Point:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;

    # will add other operators if needed

    def __add__(self, p):
        return Point(self.x+p.x, self.y+p.y)

    def __sub__(self, p):
        return Point(self.x-p.x, self.y-p.y)

    def __mul__(self, m):
        return Point(self.x*m, self.y*m)

    def __truediv__(self, m):
        return Point(self.x/m, self.y/m)

class Line:
    # hack: for vertical lines, slope is some non-finite number and h is the x
    def __init__(self, s, h):
        self.s = s
        self.h = h

    def perp_slope(self):
        if isinf(self.s):
            return 0
        return -1/self.s if self.s != 0 else inf

    def go_through_points(self, a, b):
        self.s = (b.y-a.y)/(b.x-a.x) if b.x != a.x else inf
        self.h = a.y - self.s*a.x
        if isinf(self.s):
            self.h = a.x

    def go_through_point(self, p):
        if isinf(self.s):
            self.h = p.x
        else:
            self.h = p.y - self.s*p.x

    def point_above(self, p):
        if isinf(self.s):
            return p.x > self.h
        return p.y > self.s*p.x+self.h

    def intersection(self, l):
        if self.s == l.s:
            return Point(nan, nan)
        if isinf(self.s):
            return Point(self.h, l.s*self.h+l.h)
        if isinf(l.s):
            return Point(l.h, self.s*l.h+self.h)
        return Point( (l.h-self.h)/(self.s-l.s), (self.s*l.h-l.s*self.h)/(self.s-l.s) )

    def reflect(self, p):
        l = Line(self.perp_slope(), 0)
        l.go_through_point(p)
        o = self.intersection(l)
        return o*2-p

class Fold:
    def __init__(self, f, t):
        l = Line(0, 0)
        l.go_through_points(f, t)
        self.line = Line(l.perp_slope(), 0)
        self.line.go_through_point((f+t)/2)
        self.above = self.line.point_above(f)

class Polygon:
    def __init__(self, *vertices):
        self.vertices = list(vertices)

class Page:
    def __init__(self, *vertices):
        self.original = Polygon(*vertices)
        self.folded = False
        self.part1 = self.original
        self.part2 = Polygon()

    def add_fold(self, f):
        crossed = setm = setn = False
        vp = self.original.vertices[-1]
        for v in self.original.vertices:
            l = Line(0, 0)
            l.go_through_points(vp, v)
            inter = f.line.intersection(l)
            if isinf(inter.x+inter.y):
                continue
            if (min(vp.x, v.x) <= inter.x <= max(vp.x, v.x)) and (min(vp.y, v.y) <= inter.y <= max(vp.y, v.y)):
                if not setm:
                    setm = True
                    m = inter
                    mindex = vp
                else:
                    setn = True
                    n = inter
                    nindex = vp
                    break
            vp = v

        #print("m: ", m, "n:", n)
        if setm and setn:
            crossed = True
        else:
            return False

        self.part1 = Polygon()
        self.part2 = Polygon()

        self.fold = f
        self.folded = True
        for v in self.original.vertices:
            if self.fold.line.point_above(v) == self.fold.above:
                self.part1.vertices.append(self.fold.line.reflect(v))
                if v == mindex:
                    self.part2.vertices.append(n)
                    self.part2.vertices.append(m)
                if v == nindex:
                    self.part2.vertices.append(m)
                    self.part2.vertices.append(n)
            else:
                self.part2.vertices.append(v)
                if v == mindex:
                    self.part1.vertices.append(n)
                    self.part1.vertices.append(m)
                if v == nindex:
                    self.part1.vertices.append(m)
                    self.part1.vertices.append(n)

        return True
