from __future__ import division
import math

class Line(object):

    def __init__(self, pointA, pointB):
        self.a = self.ax, self.ay = pointA
        self.b = self.bx, self.by = pointB
        self.slope = self.slope()
        self.intercept = self.intercept()

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

    def intercept(self):
        return self.ay - self.slope * self.ax

    def intersect(self, line):
        '''Returns a list containing 0, 1, or 2 intersection points between the given lines. If the two lines are equal, the second line's domain and range are used to approximate intersection points.'''
        # If they have the same slope...
        if self.slope == line.slope or (math.isnan(self.slope) and math.isnan(line.slope)):
            # ...and the same intercept, they are the same line; as a simplification, return the min/max domain/range points of the second line as intersections
            if self.intercept == line.intercept or (math.isnan(self.slope) and math.isnan(line.slope)):
                return [(min(line.ax, line.bx), min(line.ay, line.by)), (max(line.ax, line.bx), max(line.ay, line.by))]
            # ...but different intercepts, there is no intersection
            else:
                return []
        # If one is vertical, the x intersection will happen there
        elif math.isnan(self.slope):
            xintersection = self.ax
        elif math.isnan(line.slope):
            xintersection = line.ax
        # Otherwise, calculate the x intersection normally
        else:
            xintersection = (line.intercept - self.intercept) / (self.slope - line.slope)

        yintersection = self.slope * xintersection + self.intercept
        intersection = (xintersection, yintersection)

        return [intersection]
