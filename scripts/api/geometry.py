from operator import itemgetter

class RayCaster(object):

    @staticmethod
    def ray_intersects_edge(point, edge):
        p1, p2 = sorted(edge, key=itemgetter(0))
        return p1.y < point.y <= p2.y and point.x <= p1.x + (point.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y)

    @staticmethod
    def polygon_intersects_point(polygon, point):
        return bool(sum(RayCaster.ray_intersects_edge(point, edge) for edge in polygon.edges) & 1)

from collections import namedtuple

Point = namedtuple('Point', 'x, y')
Edge = namedtuple('Edge', 'p1, p2')

class Polygon(object):

    def __init__(self, boundary, name=None):
        self.name = name
        self.edges = [Edge(p1=Point(x=boundary[i][0], y=boundary[i][1]),
                           p2=Point(x=boundary[i + 1][0], y=boundary[i + 1][1]))
                      for i in range(-1, len(boundary) - 1)]

    intersects = RayCaster.polygon_intersects_point
