from __future__ import division
import math

class Line(object):

    def __init__(self, pointA, pointB):
        self.a = self.ax, self.ay = pointA
        self.b = self.bx, self.by = pointB
        self.slope = self.slope()
        self.yintercept = self.yintercept()

    def __str__(self):
        return "Line(({}, {}), ({}, {}))".format(self.a[0], self.a[1], self.b[0], self.b[1])

    def slope(self):
        xdiff = self.bx - self.ax
        ydiff = self.by - self.ay

        if xdiff == 0:
            slope = float('nan')
        else:
            slope = ydiff / xdiff

        return slope

    def yintercept(self):
        return self.ay - self.slope * self.ax

    def intersect(self, line):
        '''Returns a list containing 0, 1, or 2 intersection points between the given lines. If the two lines are equal, the first line's endpoints are returned as intersection points.'''
        # If they have the same slope...
        if self.slope == line.slope:
            # ...and the same yintercept, they are the same line; as a simplification, return the endpoints of the first line as intersections
            if self.yintercept == line.yintercept or (math.isnan(self.slope) and math.isnan(line.slope)):
                return [self.a, self.b]
            # ...but different yintercepts, there is no intersection
            else:
                return []
        # If they are both vertical...
        elif math.isnan(self.slope) and math.isnan(line.slope):
            # ...and have same xintercept, they are the same line; as a simplification, return the endpoints of the first line as intersections
            if self.ax == line.ax:
                return [self.a, self.b]
            # ...but have different xintercepts, there is no intersection
            else:
                return []
        # If one is vertical, the x intersection will happen there
        elif math.isnan(self.slope):
            xintersection = self.ax
        elif math.isnan(line.slope):
            xintersection = line.ax
        # Otherwise, calculate the x intersection normally
        else:
            xintersection = (line.yintercept - self.yintercept) / (self.slope - line.slope)

        yintersection = self.slope * xintersection + self.yintercept
        intersection = (xintersection, yintersection)

        return [intersection]
