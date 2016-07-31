from collections import namedtuple

Point = namedtuple('Point', 'x, y')
Edge = namedtuple('Edge', 'p1, p2')
Polygon = namedtuple('Polygon', 'name, edges')

class RayCaster(object):

    def __init__(self, polygons):
        self.polygons = polygons

    def _ray_intersects_edge(self, point, edge):
        p1, p2 = sorted(edge, key=lambda p: p.y)
        if point.y == p1.y or point.y == p2.y:
            return 2 * point.y - (p1.y + p2.y) > 0
        elif point.y < p2.y and point.y > p1.y:
            slope = (p2.y - p1.y) / (p2.x - p1.x)
            return point.x <= (p1.x + (point.y - p1.y) / slope)

    def _point_in_polygon(self, point, polygon):
        return bool(sum(self._ray_intersects_edge(point, edge) for edge in polygon.edges) & 1)

    def get_polygon_containing_point(self, point):
        for polygon in self.polygons:
            if self._point_in_polygon(point, polygon):
                return polygon
