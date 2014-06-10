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
        intersections = []
        for subline in self.getLines():
            intersections.append(subline.intersect(line))
        return intersections
