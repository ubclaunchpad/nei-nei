import sys
import json
from collections import namedtuple

# Tuple objects
Pos     = namedtuple('Pos', 'latitude, longitude')
Edge    = namedtuple('Edge', 'pos_a, pos_b')
Polygon = namedtuple('Polygon', 'name, edges')


class RayCaster():
    """Initialization objects for finding points in a polygon
        @param epsilon: """
    epsilon   = float(1.0e-10)
    float_min = sys.float_info.min
    float_max = sys.float_info.max

    # Does a ray cast from a pos from right to left intersect an edge?
    @classmethod
    def is_intersecting_edge(cls, pos, edge):
        # Unpack edge into positions
        pos_a, pos_b = edge
        # Have pos_a be smallest, pos_b be largest latitude, to simplify calculations
        if pos_a.latitude > pos_b.latitude:
            pos_a, pos_b = pos_b, pos_a
        # Recalculate position if orthogonal to an edge with slope == 0, as multiple other orthogonal edges would be intersected spuriously
        if pos.latitude == pos_a.latitude or pos.latitude == pos_b.latitude:
            pos = Pos(pos.latitude + cls.epsilon, pos.longitude)

        intersect_flag = False

        # If point is to the right of the edge, outside the edge range, or on an endpoint, the ray cast from that point does not intersect the edge
        if pos.longitude > max(pos_a.longitude, pos_b.longitude) or pos.latitude > pos_b.latitude or pos.latitude < pos_a.latitude:
            return intersect_flag
        # Because the point must be within the longitude range, then if the point lies to the left of the edge it intersects that edge
        if pos.longitude < min(pos_a.longitude, pos_b.longitude):
            intersect_flag = True
        # Otherwise the point lies between pos_a and pos_b longitudinally
        # So we compare slopes. The slope of a intersecting point will always be greater:
        #
        #    o (pos_a)           infinity                   o (pos_a)
        #    |\     increase <--(--) | (++)--> decrease    /
        #    | \      slope          |         slope      /
        #    |  \     |              |                   /
        # (in) o \ o (out)           |          (in) o  /  o (out)
        #    |    \   |              |                 /
        #    |     o (in)            |                o (in)
        #    |      \ |              |               /
        #    |       \|              |              /
        #    |        o (pos_b)                    o (pos_b)
        #
        # If the difference between edge endpoints or pos_a and pos is <= float_min, their respective slopes approach infinity and are considered on the edge
        else:
            if abs(pos_a.longitude - pos_b.longitude) > cls.float_min:
                base_slope = float(pos_a.latitude - pos_b.latitude) / float(pos_a.longitude - pos_b.longitude)
            else:
                base_slope = cls.float_max

            if abs(pos_a.longitude - pos.longitude) > cls.float_min:
                pos_slope = float(pos_a.latitude - pos.latitude) / float(pos_a.longitude - pos.longitude)
            else:
                pos_slope = cls.float_max

            intersect_flag = pos_slope <= base_slope
        return intersect_flag

    # Check if point resides within a full polygon by casting ray from point through polygon
    #   If number of edges intersected is odd, the point resides within the polygon, else outside
    #            __________________
    #            |                |
    #  (out) o --|----------------|------> (2 passes through)
    #            |                |
    #            | (in) o --------|------> (1 pass through)
    #            |                |
    #            |________________|
    #
    @staticmethod
    def pos_within_polygon(pos, polygon):
        return (sum(RayCaster.is_intersecting_edge(pos, edge) for edge in polygon.edges)) % 2 == 1

    # Outputs positions in JSON format (list of dicts) per polygon
    @staticmethod
    def place_pos_in_polygon(posting_list, poly_list, out_list):
        for poly in poly_list:
            poly_name = poly[0]
            postings_within_poly = []
            for posting in list(posting_list):
                pos = Pos(latitude=float(posting['lat']),
                          longitude=float(posting['lng']))
                # Determine whether position is within a polygon
                if RayCaster.pos_within_polygon(pos, poly):
                    postings_within_poly.append(posting)
                    # Remove to account for placement
                    posting_list.remove(posting)
                del pos
            # Create a list of dictionaries with neighbourhood's name and a list of postings
            poly_dict = {
                'name':      poly_name,
                'positions': postings_within_poly
            }
            out_list.append(poly_dict)
        # Create a special dict for all other positions, add to out_list
        out_list.append({
            'name':      'Outside',
            'positions': posting_list
        })

# Create polygons using edges and edges using positions, from a JSON source
def organize_polygons(polygon_edge_coords, out_list):
    for poly in polygon_edge_coords:
        new_poly  = poly['boundary']
        new_name  = poly['name']
        new_edges = ()
        # Note: lat an longitude are reversed in JSON file, so they are switched them here
        for i in range(0, len(new_poly) - 1):
            pos_a = Pos(latitude=float(new_poly[i]['longitude']),
                        longitude=float(new_poly[i]['latitude']))
            pos_b = Pos(latitude=float(new_poly[i + 1]['longitude']),
                        longitude=float(new_poly[i + 1]['latitude']))
            new_edges += (Edge(pos_a, pos_b),)
        # Join first pos to last to complete the polygon
        #   Note: first and last pos's may be the same point
        new_edges += (Edge(
            Pos(latitude=float(new_poly[-1]['longitude']),
                longitude=float(new_poly[-1]['latitude'])),
            Pos(latitude=float(new_poly[0]['longitude']),
                longitude=float(new_poly[0]['latitude']))),
            )
        out_list.append(Polygon(new_name, new_edges))


#                            Generate tuples
#
# Note: sample usage. Place these scripts into backend when using real data
# -------------------------------------------------------------------------
# polygons = []
# organize_polygons(ndata, polygons)
# out_list = []
# RayCaster.place_pos_in_polygon(in_list, polygons, out_list)
