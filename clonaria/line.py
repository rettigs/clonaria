from __future__ import division
import math

class Line(object):

    def __init__(self, pointA, pointB):
        self.a = self.ax, self.ay = pointA
        self.b = self.bx, self.by = pointB
        self.slope = self.slope()
        self.intercept = self.intercept()

    def __str__(self):
        return "({}, {}) <=> ({}, {})".format(self.a[0], self.a[1], self.b[0], self.b[1])

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
        # If they have the same slope, there is no intersection
        if self.slope == line.slope or (math.isnan(self.slope) and math.isnan(line.slope)):
            return None
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

        return intersection
