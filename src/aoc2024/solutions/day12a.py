import shapely

from collections import defaultdict
from typing import Generator


def parse_fields(farm_map:str) -> Generator[shapely.Polygon, None, None]:
    field_plots = defaultdict(list)

    for y,line in enumerate(farm_map.splitlines()):
        for x,crop in enumerate(line):
            vertices = ((x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1))
            field_plots[crop].append(shapely.Polygon(vertices))
    
    for plots in field_plots.values():
        fields = shapely.coverage_union_all(plots)
        
        yield from shapely.get_parts(fields)


def get_fence_price(field:shapely.Polygon) -> int:
    return int(field.boundary.length * field.area)


def solve(_input:str) -> int:
    fields = parse_fields(_input)

    return sum(map(get_fence_price, fields))