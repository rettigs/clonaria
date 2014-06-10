from line import Line

class Polygon(object):
    
    def __init__(self, points):
        self.points = points

    def getLines(self):
        lines = []
        for i in xrange(len(self.points)):
            lines.append(Line(self.points[i-1], self.points[i]))
        return lines

    def intersectLine(self, line):
        '''Returns a list of intersection points between the lines of the given polygon and given line.'''
        intersections = []
        for polyline in self.getLines():
            intersections + polyline.intersect(line)
        return intersections
