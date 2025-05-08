"""Shapely operations for GIS MCP server."""

from typing import Dict, Any, List, Union
from shapely import wkt
from shapely.geometry import shape, Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon
from shapely.ops import transform, unary_union, triangulate, voronoi_diagram
from shapely.affinity import rotate, scale, translate, skew

def buffer(params: Dict[str, Any]) -> str:
    """Create a buffer around a geometry."""
    geom = wkt.loads(params["geometry"])
    buffered = geom.buffer(
        distance=float(params["distance"]),
        resolution=int(params.get("resolution", 16)),
        join_style=params.get("join_style", 1),
        mitre_limit=params.get("mitre_limit", 5.0),
        single_sided=params.get("single_sided", False)
    )
    return buffered.wkt

def intersection(params: Dict[str, Any]) -> str:
    """Find intersection of two geometries."""
    geom1 = wkt.loads(params["geometry1"])
    geom2 = wkt.loads(params["geometry2"])
    result = geom1.intersection(geom2)
    return result.wkt

def union(params: Dict[str, Any]) -> str:
    """Combine two geometries."""
    geom1 = wkt.loads(params["geometry1"])
    geom2 = wkt.loads(params["geometry2"])
    result = geom1.union(geom2)
    return result.wkt

def difference(params: Dict[str, Any]) -> str:
    """Find difference between geometries."""
    geom1 = wkt.loads(params["geometry1"])
    geom2 = wkt.loads(params["geometry2"])
    result = geom1.difference(geom2)
    return result.wkt

def symmetric_difference(params: Dict[str, Any]) -> str:
    """Find symmetric difference between geometries."""
    geom1 = wkt.loads(params["geometry1"])
    geom2 = wkt.loads(params["geometry2"])
    result = geom1.symmetric_difference(geom2)
    return result.wkt

def convex_hull(params: Dict[str, Any]) -> str:
    """Calculate convex hull of a geometry."""
    geom = wkt.loads(params["geometry"])
    result = geom.convex_hull
    return result.wkt

def envelope(params: Dict[str, Any]) -> str:
    """Get bounding box of a geometry."""
    geom = wkt.loads(params["geometry"])
    result = geom.envelope
    return result.wkt

def minimum_rotated_rectangle(params: Dict[str, Any]) -> str:
    """Get minimum rotated rectangle of a geometry."""
    geom = wkt.loads(params["geometry"])
    result = geom.minimum_rotated_rectangle
    return result.wkt

def rotate_geometry(params: Dict[str, Any]) -> str:
    """Rotate a geometry."""
    geom = wkt.loads(params["geometry"])
    result = rotate(
        geom,
        angle=float(params["angle"]),
        origin=params.get("origin", "center"),
        use_radians=params.get("use_radians", False)
    )
    return result.wkt

def scale_geometry(params: Dict[str, Any]) -> str:
    """Scale a geometry."""
    geom = wkt.loads(params["geometry"])
    result = scale(
        geom,
        xfact=float(params["xfact"]),
        yfact=float(params["yfact"]),
        origin=params.get("origin", "center")
    )
    return result.wkt

def translate_geometry(params: Dict[str, Any]) -> str:
    """Translate a geometry."""
    geom = wkt.loads(params["geometry"])
    result = translate(
        geom,
        xoff=float(params["xoff"]),
        yoff=float(params["yoff"]),
        zoff=float(params.get("zoff", 0.0))
    )
    return result.wkt

def triangulate_geometry(params: Dict[str, Any]) -> List[str]:
    """Create a triangulation of a geometry."""
    geom = wkt.loads(params["geometry"])
    triangles = triangulate(geom)
    return [tri.wkt for tri in triangles]

def voronoi(params: Dict[str, Any]) -> str:
    """Create a Voronoi diagram from points."""
    geom = wkt.loads(params["geometry"])
    result = voronoi_diagram(geom)
    return result.wkt

def unary_union_geometries(params: Dict[str, Any]) -> str:
    """Create a union of multiple geometries."""
    geoms = [wkt.loads(g) for g in params["geometries"]]
    result = unary_union(geoms)
    return result.wkt

def get_centroid(params: Dict[str, Any]) -> str:
    """Get the centroid of a geometry."""
    geom = wkt.loads(params["geometry"])
    result = geom.centroid
    return result.wkt

def get_length(params: Dict[str, Any]) -> float:
    """Get the length of a geometry."""
    geom = wkt.loads(params["geometry"])
    return float(geom.length)

def get_area(params: Dict[str, Any]) -> float:
    """Get the area of a geometry."""
    geom = wkt.loads(params["geometry"])
    return float(geom.area)

def get_bounds(params: Dict[str, Any]) -> List[float]:
    """Get the bounds of a geometry."""
    geom = wkt.loads(params["geometry"])
    return list(geom.bounds)

def get_coordinates(params: Dict[str, Any]) -> List[List[float]]:
    """Get the coordinates of a geometry."""
    geom = wkt.loads(params["geometry"])
    return [list(coord) for coord in geom.coords]

def get_geometry_type(params: Dict[str, Any]) -> str:
    """Get the type of a geometry."""
    geom = wkt.loads(params["geometry"])
    return geom.geom_type

def is_valid(params: Dict[str, Any]) -> bool:
    """Check if a geometry is valid."""
    geom = wkt.loads(params["geometry"])
    return bool(geom.is_valid)

def make_valid(params: Dict[str, Any]) -> str:
    """Make a geometry valid."""
    geom = wkt.loads(params["geometry"])
    result = geom.make_valid()
    return result.wkt

def simplify(params: Dict[str, Any]) -> str:
    """Simplify a geometry."""
    geom = wkt.loads(params["geometry"])
    result = geom.simplify(
        tolerance=float(params["tolerance"]),
        preserve_topology=params.get("preserve_topology", True)
    )
    return result.wkt 