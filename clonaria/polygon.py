from __future__ import division
from line import Line

class Polygon(object):
    
    def __init__(self, points):
        self.points = points

    def __str__(self):
        return "Polygon({})".format(self.points)

    def getLines(self):
        lines = []
        for i in xrange(len(self.points)):
            lines.append(Line(self.points[i-1], self.points[i]))
        return lines

    def intersectLine(self, line):
        '''Returns a list of intersection points between the lines of the given polygon and given line.'''
        intersections = []
        for polyline in self.getLines():
            intersections.extend(polyline.intersect(line))
        return intersections

    def translate(self, (x, y)):
        self.points = [(px+x, py+y) for px, py in self.points]
        return self
