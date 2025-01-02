import shapely

from .day12a import parse_fields

def count_polygon_sides(polygon:shapely.Polygon) -> int:
    side_count = 0

    for ring in shapely.get_rings(polygon):
        ring = ring.simplify(0)
        joint = shapely.LineString(ring.coords[-2:] + ring.coords[:2]).simplify(0)

        side_count += len(ring.coords) + len(joint.coords) - 4

    return side_count


def get_fence_price(field:shapely.Polygon) -> int:
    return int(count_polygon_sides(field) * field.area)


def solve(_input:str) -> int:
    fields = parse_fields(_input)

    return sum(map(get_fence_price, fields))