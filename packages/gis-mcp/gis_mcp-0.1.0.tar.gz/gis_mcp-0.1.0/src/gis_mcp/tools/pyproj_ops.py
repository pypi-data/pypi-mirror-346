"""PyProj operations for GIS MCP server."""

from typing import Dict, Any, List, Tuple, Union
import pyproj
from shapely import wkt
from shapely.ops import transform

def transform_coordinates(params: Dict[str, Any]) -> List[float]:
    """Transform coordinates between CRS."""
    transformer = pyproj.Transformer.from_crs(
        params["source_crs"],
        params["target_crs"],
        always_xy=True
    )
    x, y = params["coordinates"]
    x_transformed, y_transformed = transformer.transform(x, y)
    return [x_transformed, y_transformed]

def project_geometry(params: Dict[str, Any]) -> str:
    """Project a geometry between CRS."""
    geom = wkt.loads(params["geometry"])
    transformer = pyproj.Transformer.from_crs(
        params["source_crs"],
        params["target_crs"],
        always_xy=True
    )
    projected = transform(transformer.transform, geom)
    return projected.wkt

def get_crs_info(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get information about a CRS."""
    crs = pyproj.CRS(params["crs"])
    return {
        "name": crs.name,
        "type": crs.type_name,
        "axis_info": [axis.direction for axis in crs.axis_info],
        "is_geographic": crs.is_geographic,
        "is_projected": crs.is_projected,
        "datum": str(crs.datum),
        "ellipsoid": str(crs.ellipsoid),
        "prime_meridian": str(crs.prime_meridian),
        "area_of_use": str(crs.area_of_use) if crs.area_of_use else None
    }

def get_available_crs(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get list of available CRS."""
    crs_list = []
    for crs in pyproj.database.get_crs_list():
        try:
            crs_info = get_crs_info({"crs": crs})
            crs_list.append({
                "auth_name": crs.auth_name,
                "code": crs.code,
                "name": crs_info["name"],
                "type": crs_info["type"]
            })
        except:
            continue
    return crs_list

def get_geod_info(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get information about a geodetic calculation."""
    geod = pyproj.Geod(
        ellps=params.get("ellps", "WGS84"),
        a=params.get("a"),
        b=params.get("b"),
        f=params.get("f")
    )
    return {
        "ellps": geod.ellps,
        "a": geod.a,
        "b": geod.b,
        "f": geod.f,
        "es": geod.es,
        "e": geod.e
    }

def calculate_geodetic_distance(params: Dict[str, Any]) -> Dict[str, float]:
    """Calculate geodetic distance between points."""
    geod = pyproj.Geod(ellps=params.get("ellps", "WGS84"))
    lon1, lat1 = params["point1"]
    lon2, lat2 = params["point2"]
    forward_azimuth, back_azimuth, distance = geod.inv(lon1, lat1, lon2, lat2)
    return {
        "distance": distance,
        "forward_azimuth": forward_azimuth,
        "back_azimuth": back_azimuth
    }

def calculate_geodetic_point(params: Dict[str, Any]) -> List[float]:
    """Calculate point at given distance and azimuth."""
    geod = pyproj.Geod(ellps=params.get("ellps", "WGS84"))
    lon, lat = params["start_point"]
    forward_azimuth = params["azimuth"]
    distance = params["distance"]
    lon2, lat2, back_azimuth = geod.fwd(lon, lat, forward_azimuth, distance)
    return [lon2, lat2]

def calculate_geodetic_area(params: Dict[str, Any]) -> float:
    """Calculate area of a polygon using geodetic calculations."""
    geod = pyproj.Geod(ellps=params.get("ellps", "WGS84"))
    polygon = wkt.loads(params["geometry"])
    area = abs(geod.geometry_area_perimeter(polygon)[0])
    return float(area)

def get_utm_zone(params: Dict[str, Any]) -> str:
    """Get UTM zone for given coordinates."""
    lon, lat = params["coordinates"]
    return pyproj.database.query_utm_crs_info(
        datum_name="WGS84",
        area_of_interest=pyproj.aoi.AreaOfInterest(
            west_lon_degree=lon,
            south_lat_degree=lat,
            east_lon_degree=lon,
            north_lat_degree=lat
        )
    )[0].to_authority()[1]

def get_utm_crs(params: Dict[str, Any]) -> str:
    """Get UTM CRS for given coordinates."""
    lon, lat = params["coordinates"]
    return pyproj.database.query_utm_crs_info(
        datum_name="WGS84",
        area_of_interest=pyproj.aoi.AreaOfInterest(
            west_lon_degree=lon,
            south_lat_degree=lat,
            east_lon_degree=lon,
            north_lat_degree=lat
        )
    )[0].to_wkt()

def get_geocentric_crs(params: Dict[str, Any]) -> str:
    """Get geocentric CRS for given coordinates."""
    lon, lat = params["coordinates"]
    return pyproj.database.query_geocentric_crs_info(
        datum_name="WGS84",
        area_of_interest=pyproj.aoi.AreaOfInterest(
            west_lon_degree=lon,
            south_lat_degree=lat,
            east_lon_degree=lon,
            north_lat_degree=lat
        )
    )[0].to_wkt() 