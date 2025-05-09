"""Utility script containing functions used for flowtrace and splitcatchment modules."""
import json
import math
import os
import sys
import urllib.parse
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import TypedDict
from typing import Union

import numpy as np
import pyflwdir
import pyproj
import rasterio.mask
import rasterio.profiles
import requests
from shapely.geometry import GeometryCollection
from shapely.geometry import LineString
from shapely.geometry import MultiPolygon
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import shape
from shapely.ops import split
from shapely.ops import transform
from shapely.ops import unary_union

from . import logger


# Service endpoints
NLDI_URL = "https://api.water.usgs.gov/nldi/linked-data/comid/"
NLDI_GEOSERVER_URL = "https://api.water.usgs.gov/geoserver/wmadata/ows"
IN_FDR_COG = os.environ.get(
    "COG_URL",
    "/vsicurl/https://prod-is-usgs-sb-prod-publish.s3.amazonaws.com/5fe0d98dd34e30b9123eedb0/fdr.tif",
)
IN_FAC_COG = os.environ.get(
    "COG_URL",
    "/vsicurl/https://prod-is-usgs-sb-prod-publish.s3.amazonaws.com/5fe0d98dd34e30b9123eedb0/fac.tif",
)

# Hard coding the CRS for the NHD and rasters being used
wgs84 = pyproj.CRS("EPSG:4326")
dest_crs = pyproj.CRS("EPSG:5070")


# Classes defining JSON object type
class JsonFeatureType(TypedDict):
    """Custom Class defining a Json feature."""

    type: str
    id: str
    geometry: dict[str, Union[list[list[list[float]]], str]]
    geometry_name: str
    properties: dict[Union[str, int, float, None], Union[str, int, float, None]]
    bbox: list[float]


class JsonFeatureCollectionType(TypedDict):
    """Custom Class defining a Json feature collection."""

    type: str
    features: list[JsonFeatureType]
    totalFeatures: str  # noqa N815
    numberReturned: int  # noqa N815
    timeStamp: str  # noqa N815
    crs: dict[str, Union[str, dict[str, str]]]
    bbox: list[float]


# functions
def get_coordsys() -> Tuple[pyproj.Transformer, pyproj.Transformer]:
    """Get coordinate system of input flow direction raster.

    Currently, the CRS of the raster is hard coded as EPGS:5070. This function returns to
    pyproj transformer objects: one projecting from EPSG:4326 to EPSG:5070, and the other
    transformer is vice versa.

    Returns:
        A tuple of pyproj transformers: one projecting from EPSG:4326 to EPSG:5070, and the
        other transformer is vice versa.
    """
    transform_to_raster = pyproj.Transformer.from_crs(wgs84, dest_crs, always_xy=True)
    transform_to_wgs84 = pyproj.Transformer.from_crs(dest_crs, wgs84, always_xy=True)

    return transform_to_raster, transform_to_wgs84


def check_coords(x: float, y: float) -> None:
    """Check the submitted point is formatted correctly, and inside CONUS.

    Takes in a x, y coordinate pair as lon, lat in WGS. Checks to make sure the x coord
    is positive and that the y coord is negative. Also checks to make sure the coordinate
    pair is within the bounding box of CONUS. If the coords do not match these checks, then
    this function will end the processing of this point.

    Args:
        x (float): The x coordinate in WGS84, AKA: Longitude.
        y (float): The y coordinate in WGS84, AKA: Latitude.
    """
    if x > 0 or y < 0:
        logger.critical(
            "Improper coordinates submitted. Makes sure the coords are submitted "
            "as longitude, latitude in WGS 84 decimal degrees."
        )
        # Kill program if point is not lon, lat.
        sys.exit(1)
    elif not -124.848974 < x < -66.885444 or not 24.396308 < y < 49.384358:
        logger.critical(
            "Coordinates outside of CONUS. Submit a point within (-124.848974, "
            "24.396308) and (-66.885444, 49.384358)."
        )
        # Kill program if point is outside CONUS.
        sys.exit(1)
    else:
        logger.info("Point is correctly formatted and within the bounding box of CONUS.")


def transform_geom(
    proj: pyproj.Transformer, geom: Union[MultiPolygon | Polygon | Point | LineString]
) -> Union[MultiPolygon | Polygon | Point | LineString]:
    """Transform geometry to input projection.

    Args:
        proj (pyproj.Transformer): A pyproj transformer object providing the to and
            from coordinate reference systems info.
        geom (MultiPolygon | Polygon | Point | LineString): The Shapely geometry to reproject.

    Returns:
        A Shapely geometry in the specified CRS.
    """
    # This is necessary to prevent pyproj.transform from outputting 'inf' values
    # os.environ["PROJ_NETWORK"] = "OFF"
    projected_geom = transform(proj.transform, geom)
    projected_geom = transform(proj.transform, geom)

    return projected_geom


def get_local_catchment(x: float, y: float) -> Tuple[str, Union[MultiPolygon, Polygon]]:
    """Perform point in polygon query to NLDI geoserver to get local catchment geometry.

    Args:
        x (float): The x coordinate in WGS84, AKA: Longitude.
        y (float): The y coordinate in WGS84, AKA: Latitude.

    Returns:
        A tuple containg a string of the NHD catchment ID number which the XY query point falls within
        and a shapely geometry of the NHD catchment.

    Raises:
        ValueError: Returns an error if the query to the NLDI Geoserver fails.
        IndexError: Returns an error the query to the GeoServer worked, but the responce did not have a catchment.
    """
    logger.info("requesting local catchment...")
    wkt_point = f"POINT({x} {y})"
    cql_filter = f"INTERSECTS(the_geom, {wkt_point})"

    payload = {
        "service": "wfs",
        "version": "1.0.0",
        "request": "GetFeature",
        "typeName": "wmadata:catchmentsp",
        "outputFormat": "application/json",
        "srsName": "EPSG:4326",
        "CQL_FILTER": cql_filter,
    }

    # Convert spaces in query to '%20' instead of '+'
    fixed_payload: str = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)

    # request catchment geometry from point in polygon query from NLDI geoserver
    r: requests.models.Response = requests.get(NLDI_GEOSERVER_URL, params=fixed_payload, timeout=5)
    try:
        # Try to  convert response to json
        resp = r.json()
        try:
            # get catchment id
            catchment_id = json.dumps(resp["features"][0]["properties"]["featureid"])
        except IndexError:
            raise IndexError("The NLDI GeoServer failed to return a catchment.") from None
    except ValueError:
        raise ValueError(
            "Quitting nldi_flowtools query. Error requesting local basin from the NLDI GeoServer:",
            "Status code:",
            r.status_code,
            "Error message:",
            r.reason,
        ) from None

    features = resp["features"][0]
    number_of_polygons = len(features["geometry"]["coordinates"])
    if number_of_polygons > 1:  # Catchments can be multipoly (I know, this is SUPER annoying)
        logger.warning(
            f"Multipolygon catchment found: \
                {json.dumps(features['properties']['featureid'])} \
                Number of polygons: {number_of_polygons}"
        )
        i: int = 0
        catchment_geom = []
        while i < number_of_polygons:
            catchment_geom.append(Polygon(features["geometry"]["coordinates"][i][0]))
            i += 1
        catchment_geom = MultiPolygon(catchment_geom)
    else:  # Else, the catchment is a single polygon (as it should be)
        catchment_geom = Polygon(features["geometry"]["coordinates"][0][0])

    logger.info(f"got local catchment: {catchment_id}")
    return catchment_id, catchment_geom


def get_local_flowline(
    catchment_id: str,
) -> Tuple[JsonFeatureCollectionType, LineString]:
    """Request the NHD Flowline from NLDI with the Catchment ID.

    With the catchment ID, makes a get request to the NLDI service for the geometry of
    the local NHD flowline.

    Args:
        catchment_id (str): A string of the ID number for the NHD catchment.

    Returns:
        A tuple containing the raw JSON and a Shapely LineString of the local NHD
        flowline. The flowline geometry is converted from 3D to 2D.

    Raises:
        ValueError: Returns an error if the query to the NLDI Geoserver fails.
        IndexError: Returns an error the query to the GeoServer worked, but the responce did not have a flowline.
    """
    cql_filter = f"comid={catchment_id}"

    payload = {
        "service": "wfs",
        "version": "1.0.0",
        "request": "GetFeature",
        "typeName": "wmadata:nhdflowline_network",
        "maxFeatures": "500",
        "outputFormat": "application/json",
        "srsName": "EPSG:4326",
        "CQL_FILTER": cql_filter,
    }
    # Convert spaces in query to '%20' instead of '+'
    fixed_payload = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)

    # request flowline geometry from NLDI geoserver using catchment ID
    r: requests.models.Response = requests.get(NLDI_GEOSERVER_URL, params=fixed_payload, timeout=5)
    try:
        # Try to  convert response to json
        flowline_json = r.json()
        try:
            # check json response for geometry
            nhd_geom = flowline_json["features"][0]["geometry"]
            # logger.info("got local flowline")
        except IndexError:
            raise IndexError("The NLDI GeoServer failed to return a flowline.") from None
    except ValueError:
        raise ValueError(
            "Quitting nldi_flowtools query. Error requesting local flowline from the NLDI GeoServer:",
            "Status code:",
            r.status_code,
            "Error message:",
            r.reason,
        ) from None

    # Convert xyz to xy and return as a shapely LineString
    flowline_geom = LineString([i[0:2] for i in nhd_geom["coordinates"][0]])

    return flowline_json, flowline_geom


def get_total_basin(catchment_id: str) -> GeometryCollection:
    """Use a catchment identifier to get the upstream basin geometry from NLDI.

    With the catchment ID, make a Get request to the NLDI service for the geometry of
    the upstream drainage basin from an NHD catchment.

    Args:
        catchment_id (str): A string of the ID number for the NHD catchment.

    Returns:
        A GeometryCollection containing the geometry of and other info about the
        upstream basin.

    Raises:
        ValueError: Returns an error if the query to the NLDI Geoserver fails.
        IndexError: Returns an error the query to the GeoServer worked, but the responce did not have a basin.
    """
    logger.info("getting upstream basin...")

    # request upstream basin
    payload = {"f": "json", "simplified": "false"}

    # request upstream basin from NLDI using comid of catchment point is in
    r: requests.models.Response = requests.get(NLDI_URL + catchment_id + "/basin", params=payload, timeout=5)

    try:
        # Try to  convert response to json
        resp = r.json()
        try:
            # convert geojson to ogr geom
            features = resp["features"]
            total_basin_geom = GeometryCollection([shape(feature["geometry"]).buffer(0) for feature in features])
        except IndexError:
            raise IndexError("The NLDI failed to return a drainage base.") from None
    except ValueError:
        raise ValueError(
            "Quitting nldi_flowtools query. Error requesting upstream basin from the NLDI:",
            "Status code:",
            r.status_code,
            "Error message:",
            r.reason,
        ) from None

    logger.info("finished getting upstream basin")
    return total_basin_geom


def get_upstream_basin(
    catchment_geom: Union[MultiPolygon, Polygon],
    split_catchment_geom: Polygon,
    total_basin_geom: GeometryCollection,
) -> Union[MultiPolygon, Polygon]:
    """Get the upstream basin geometry.

    This is done by subtracting the local catchment geometry from the total basin geometry
    (what is returned from the NLDI basin query) and then merging this to the
    splitcatchment geometry.
    """
    # Clip the local catchment off of the total basin geometry
    upstream_basin_geom = total_basin_geom.difference(catchment_geom.buffer(0.00001))
    # Smooth out the split catchment before merging it
    simplified_split_catchment_geom = split_catchment_geom.buffer(0.0002).simplify(0.00025)
    # Merge the splitcatchment and upstream basin
    drainage_basin = simplified_split_catchment_geom.union(upstream_basin_geom.buffer(0.0002)).buffer(-0.0002)

    return drainage_basin


def project_point(x: float, y: float, transform: pyproj.Transformer) -> Tuple[float, float]:
    """Project a point to the specified CRS.

    Args:
        x (float): The x coordinate which is to be projected to a different CRS.
        y (float): The y coordinate which is to be projected to a different CRS.
        transform (pyproj.Transformer): The pyproj transformer which contains the
            from CRS and the to CRS information.

    Returns:
        A tuple of two floats representing the projected x and y coords.
    """
    point_geom: Point = Point(x, y)
    logger.info(f"original point: {point_geom.wkt}")

    projected_point = transform_geom(transform, point_geom)
    logger.info(f"projected point: {projected_point.wkt}")

    projected_xy: tuple[float, float] = projected_point.coords[:][0]

    # Test if one of the project point coordinates is infinity. If this is the case
    # then the point was not properly projected to the CRS of the DEM. This has happened
    # when proj version is greater than 6.2.1
    projected_x = projected_point.coords[:][0][0]
    if math.isinf(projected_x) is True:
        logger.critical("Input point was not properly projected. This could be an error caused by PROJ.")

    return projected_xy


def get_flowgrid(
    catchment_geom: Union[MultiPolygon, Polygon],
) -> Tuple[np.ndarray, rasterio.profiles.Profile]:
    """Get the FDR for the local catchment area.

    Use a 10 meter buffer of the local catchment to clip the
    NHD Plus v2 flow direction raster.

    Args:
        catchment_geom (Polygon or MultiPolygon): Polygon geometry for which to return the
            fdr raster.

    Returns:
        A tuple containing a Numpy array and a rasterio Profile object.
    """
    logger.info("start clip of fdr raster")
    with rasterio.open(IN_FDR_COG, "r") as ds:
        fdr_profile = ds.profile

        # buffer catchment geometry by 10m before clipping flow direction raster
        buffer_catchment_geom = GeometryCollection([catchment_geom.buffer(10)])

        # clip input fd
        flwdir, flwdir_transform = rasterio.mask.mask(ds, buffer_catchment_geom.geoms, crop=True)
        logger.info("finish clip of fdr raster")

        fdr_profile.update(
            {
                "height": flwdir.shape[1],
                "width": flwdir.shape[2],
                "transform": flwdir_transform,
            }
        )

    return flwdir, fdr_profile


def get_facgrid(
    catchment_geom: Union[MultiPolygon, Polygon],
) -> Tuple[np.ndarray, rasterio.profiles.Profile]:
    """Get the FAC for the local catchment area.

    Use a 10 meter buffer of the local catchment to clip the
    NHD Plus v2 flow accumulation raster.

    Args:
        catchment_geom (Polygon or MultiPolygon): Shapely Polygon geometry for which to
            return the fac raster.

    Returns:
        A tuple containing a Numpy array and a rasterio Profile.
    """
    logger.info("start clip of fac raster")
    with rasterio.open(IN_FAC_COG, "r") as ds:
        fac_profile = ds.profile

        # buffer catchment geometry by 10m before clipping flow direction raster
        buffer_catchment_geom = GeometryCollection([catchment_geom.buffer(10)])

        # clip input fd
        fac, fac_transform = rasterio.mask.mask(ds, buffer_catchment_geom.geoms, crop=True)

        fac_profile.update(
            {
                "height": fac.shape[1],
                "width": fac.shape[2],
                "transform": fac_transform,
            }
        )

    logger.info("finished clip of the fac raster")
    return fac, fac_profile


def split_catchment(
    xy_pair: Tuple[float, float],
    flwdir: np.ndarray,
    flwdir_transform: rasterio.Affine,
) -> Polygon:
    """Delineate a basin from an X,Y coordinate pair.

    The name for the function is split catchment since the input FDR grid is clipped
    to the local NHD catchment, so the resulting basin may not be the true drainage
    basin for the point but rather the basin within the catchment. The python package
    pyflwdir is used as the engine for the delineation.

    Args:
        xy_pair (Tuple[float, float]): A tuple of floats representing the X and Y (respectively)
            coordinates of the point to delineate. The CRS for the XY pair should match that
            of the raster.
        flwdir (np.ndarray): A 2D numpy array containing the flow direction values from which the
            basin is delineated. The FDR values should match that of the D8 ESRI format (1-128).
        flwdir_transform (rasterio.Affine): The transformation info for the FDR raster.

    Returns:
        A Shapely Polygon representing the drainage basin within the local NHD catchment. The
        splitcatchment polygon is in the same CRS as the input parameters.
    """
    logger.info("start split catchment...")

    # import clipped fdr into pyflwdir
    flw = pyflwdir.from_array(flwdir[0], ftype="d8", transform=flwdir_transform)

    # delineate subbasins
    subbasins = flw.basins(xy=xy_pair)

    # convert subbasins from uint32
    subbasins = subbasins.astype(np.int32)

    # convert raster to features
    mask = subbasins != 0
    polys = rasterio.features.shapes(subbasins, transform=flwdir_transform, mask=mask)

    # Loop thru all the polygons that are returned from pyflwdir
    transformed_polys = []
    for poly, _ in polys:
        transformed_polys.append(Polygon(poly["coordinates"][0]))

    # Merge polygons, if there are more than one
    split_geom = unary_union(transformed_polys)

    logger.info("finish split catchment.")
    return split_geom


def get_row_column(point: tuple[float, float], raster_transform: rasterio.Affine) -> Tuple[int, int]:
    """Given an x,y point and a rasterio Affine, return the indices of the raster row and column."""
    col, row = ~raster_transform * (point)
    row = int(row)
    column = int(col)

    return row, column


def get_cell_corner(row: int, column: int, raster_transform: rasterio.Affine) -> Tuple[float, float]:
    """Given a row column pair, return the coords of the top left corner of a raster cell."""
    origin_x = raster_transform[2]
    origin_y = raster_transform[5]
    cell_size = raster_transform[0]

    return (origin_x + column * cell_size), (origin_y - row * cell_size)


def get_cell_center(row: int, column: int, raster_transform: rasterio.Affine) -> Tuple[float, float]:
    """Given an row column pair, return the coordinates of the raster cell center."""
    origin_x = raster_transform[2]
    origin_y = raster_transform[5]
    cell_size = raster_transform[0]

    return (origin_x + (column + 0.5) * cell_size), (origin_y - (row + 0.5) * cell_size)


def create_cell_polygon(
    row: int,
    col: int,
    raster_transform: rasterio.Affine,
) -> Polygon:
    """Given a row, column pair and rasterio affine, return an outline of the raster cell.

    Actually, the cell polygon is 1 meter smaller than actually size. For instance, a 30m
    cell will have a 28m polygon returned. This is helpful to functions which use this one
    to determine whether a NHD Flowline is within a raster cell. If the flowline geomtery only
    intersects the cell at the very edge (1m or less), then the flowline is not considered
    to be within the cell.
    """
    top_left_x, top_left_y = get_cell_corner(row, col, raster_transform)
    top_right_x, top_right_y = get_cell_corner(row, col + 1, raster_transform)
    bottom_left_x, bottom_left_y = get_cell_corner(row + 1, col, raster_transform)
    bottom_right_x, bottom_right_y = get_cell_corner(row + 1, col + 1, raster_transform)

    cell_geom = Polygon(
        (
            (top_left_x + 1, top_left_y - 1),
            (top_right_x - 1, top_right_y - 1),
            (bottom_right_x - 1, bottom_right_y + 1),
            (bottom_left_x + 1, bottom_left_y + 1),
        )
    ).normalize()

    return cell_geom


def get_on_flowline(
    row: int,
    col: int,
    flowline: LineString,
    raster_transform: rasterio.Affine,
    fac: np.ndarray,
    fdr: np.ndarray,
) -> bool:
    """Determine whether the raster cell 'intersects' the given flowline geometry.

    This is not exactly straightforward. The cell needs to both intersect the line geoemtry
    and the Flow Accumultion value needs to be above 900. Only when both of these are true
    does the function return a boolean value of 'True'. Also, if the next downhill FAC cell has
    a value 2x greater than the current cell, the function will return False. Since the flowline
    vector geometry intersects FAC cells with low values, we want to not considered these low value
    FAC cells to be 'on' the stream line. This is important since if a basin delineation were
    to be preformed on a cell which is not on a stream cell, then the basin will not include
    all of the area that the user would expect.

    Args:
        row (int): Index for the row of the cell within the raster
        col (int): Index for the column of the cell within the raster
        flowline (LineString): The line geometry of the flowline
        raster_transform (rasterio.Affine): The transformation info of the raster
        fac (np.ndarray): The flow accumulation values as a 2D numpy array
        fdr (np.ndarray): The flow direction values as a 2D numpy array, uses ESRI flow directions

    Returns:
        A boolean value indicating where the specified raster cell passes the criteria to be
        considered a stream cell.
    """
    cell_geom = create_cell_polygon(row, col, raster_transform)
    cell_intersect = flowline.intersects(cell_geom)
    # Does the cell intersect the flowline?
    if cell_intersect:
        fac_val = fac[0][row, col]
        # Is the FAC value large?
        if fac_val > 900:
            fdr_val = fdr[0][row, col]
            down_row, down_col = get_downhill_cell(row, col, fdr_val)
            down_fac_val = fac[0][down_row, down_col]
            fac_ratio = down_fac_val / fac_val
            # Is the downhill cell FAC value significantly larger?
            # This is meant to detect whether the downhill cell is a larger stream.
            # If the downhill FAC cell is more that double the current cell, then we want to
            # keep going downhill.
            if fac_ratio < 2:
                logger.info("point is on a flowline")
                return True
            else:
                logger.info("point not on a flowline")
                return False
        else:
            logger.info("point not on a flowline")
            return False
    else:
        logger.info("point not on a flowline")
        return False


def get_downhill_cell(row: int, col: int, fdr_val: np.uint8) -> Tuple[int, int]:
    # noqa: DAR401
    """Return the row, column indices of the next cell downhill given the flow direction.

    Args:
        row (int): The cell row index.
        col (int): The cell column index.
        fdr_val (np.uint8): The cell flow direction value in the D8 ESRI format.

    Returns:
        A tuple containing the row, column indices of the downhill FDR cell.
    """
    if fdr_val == 128:  # NE
        return row - 1, col + 1

    elif fdr_val == 64:  # N
        return row - 1, col

    elif fdr_val == 32:  # NW
        return row - 1, col - 1

    elif fdr_val == 16:  # W
        return row, col - 1

    elif fdr_val == 8:  # SW
        return row + 1, col - 1

    elif fdr_val == 4:  # S
        return row + 1, col

    elif fdr_val == 2:  # SE
        return row + 1, col + 1

    elif fdr_val == 1:  # E
        return row, col + 1

    else:
        raise ValueError("Flowtrace intersected a nodata FDR value; cannot continue downhill.")


def trace_downhill(
    point: tuple[float, float],
    raster_transform: rasterio.Affine,
    fdr: np.array,
    fac: np.array,
    flowline_geom: LineString,
    catchment_geom: Polygon,
    transform_to_wgs84: pyproj.Transformer,
    transform_to_raster: pyproj.Transformer,
) -> Tuple[List[Tuple[float, float]], List[Any]]:
    """Given a starting point, trace down the flow direction grid.

    The function returns a list of x,y coords. The first coord pair is the input
    coord. The next is the cell center of the cell the point falls in. As the trace
    proceeds downhill, each cell center gets added to the coord list.
    Once the trace gets to a cell that overlaps the input flowline geometry and the
    flow accumulation value is greater that 900, then the trace stops. The the closest
    point on the flowline geometry is grabbed and added to the coord list.
    Sometimes the flowtrace does not intersect the NHD flowline before the edge of the
    local NHD catchment. If this happens, then the function requests the next downstream
    catchment, flowline, flow direction raster and flow accumulation raster. This allows
    the downhill trace to continue until the intersection is found.

    Args:
        point (Tuple[float, float]): A x,y coordinate pair from which to start the flow trace.
        raster_transform (rasterio.Affine): The transformation info of the two input rasters.
        fdr (np.array): The flow direction raster as a numpy array.
        fac (np.array): The flow accumulation raster as a numpy array.
        flowline_geom (LineString): The stream flowline geometry.
        catchment_geom (Polygon): The geometry of the local NHD catchment.
        transform_to_wgs84 (pyproj.Transformer): PyProj transformer to project from the raster crs to WGS84.
        transform_to_raster (pyproj.Transformer): PyProj transformer to project from WGS84 to the raster crs.

    Returns:
        The first list contains x,y coordinate pairs representing the flow path from the start point to the
        flowline geoemtry.
        The seconds list which if the fist item is True, then the next two items are the downstream NHD flowline
        json and shapely geometry objects. If the first item is False, then the next two items are None.
    """
    jumped_downstream = [False, None, None]
    # The first flowpath point is the clip point
    flowpath_coords = [point]
    # Is this point on the flowline/stream cell?
    row, col = get_row_column(point, raster_transform)
    on_flowline = get_on_flowline(row, col, flowline_geom, raster_transform, fac, fdr)

    # Trace downhill until we find a stream cell
    while not on_flowline:
        # Get the flow direction
        fdr_val = fdr[0][row, col]
        # Get the the downhill cell and add it to the coords list
        try:
            row, col = get_downhill_cell(row, col, fdr_val)
            next_point = get_cell_center(row, col, raster_transform)
            # Check if this next cell is on the flowline, is so, stop the loop. If not, continue
            on_flowline = get_on_flowline(row, col, flowline_geom, raster_transform, fac, fdr)
            if not on_flowline:
                flowpath_coords.append(next_point)
        except ValueError:
            logger.warning("Flowtrace is jumping to the downstream catchment.")
            # Remove the last coordinate from the flowpath
            flowpath_coords.pop(-1)
            # Get the lon, lat coords of the current point, use this to get the local
            # catchment and flowline
            x, y = transform_geom(transform_to_wgs84, Point(next_point)).coords[0]
            catchment_id, catchment_geom = get_local_catchment(x, y)
            projected_catchment_geom = transform_geom(transform_to_raster, catchment_geom)
            flowline_json, flowline_geom_wgs84 = get_local_flowline(catchment_id)
            flowline_geom = transform_geom(transform_to_raster, flowline_geom_wgs84)
            # Query the fdr and fac grids for the new catchment
            fdr, fdr_profile = get_flowgrid(projected_catchment_geom)
            raster_transform = fdr_profile["transform"]
            fac, _ = get_facgrid(projected_catchment_geom)
            row, col = get_row_column(next_point, raster_transform)
            # Check if this current point is on the flowline/stream grid
            on_flowline = get_on_flowline(row, col, flowline_geom, raster_transform, fac, fdr)
            # Return the updated flowline info
            jumped_downstream = [True, flowline_json, flowline_geom_wgs84]

    # Clip the NHD flowline to the current raster cell
    cell_geom = create_cell_polygon(row, col, raster_transform)
    clipped_line = flowline_geom.intersection(cell_geom)
    # Take the midpoint of the clipped flowline, add to the flowpath coords
    flowpath_coords.append(clipped_line.centroid.__geo_interface__["coordinates"])

    return flowpath_coords, jumped_downstream


def get_reach_measure(
    intersection_point: Point,
    flowline: JsonFeatureCollectionType,
    raindrop_path: LineString,
) -> Dict[str, Union[Any, str, float, None]]:
    """Collect NHD Flowline Reach Code and Measure.

    All coordinates of the inputs must be in WGS84/EPSG:4326.
    This function uses the split_flowline() function to determine the distance
    of the intersection point on the NHD flowline segment. It then uses the
    resulting line geometries to calculate the Reach/Measure of the intersection
    with the NHD Flowline.

    Args:
        intersection_point (Point): The point at which to split the NHD Flowline.
        flowline (JsonFeatureCollectionType): The NHD Flowline geom and info as JSON.
        raindrop_path (LineString): The raindrop path geometry.

    Returns:
        A dictionary of information about the NHD Flowline and the intersection with it.
        Stream info includes GNIS Name, COMID, Reach Code, the intersection point in
        lon, lat coords and the length of the raindrop path.
    """
    # Set Geoid to measure distances in meters
    geod = pyproj.Geod(ellps="WGS84")

    # Convert the flowline to a geometry collection to be exported
    nhd_geom = flowline["features"][0]["geometry"]
    nhd_flowline = GeometryCollection([shape(nhd_geom)]).geoms[0]
    nhd_flowline = LineString([xy[0:2] for xy in list(nhd_flowline.geoms[0].coords)])  # Convert xyz to xy

    # Select the stream name from the NHD Flowline
    stream_name = flowline["features"][0]["properties"]["gnis_name"]
    if stream_name == " ":
        stream_name = "none"

    # Create stream_info dict and add some data
    stream_info = {
        "gnis_name": stream_name,
        "comid": flowline["features"][0]["properties"][
            "comid"
        ],  # 'lengthkm': flowline['features'][0]['properties']['lengthkm'],
        "intersection_point": (intersection_point.coords[0]),
        "reachcode": flowline["features"][0]["properties"]["reachcode"],
    }

    # Add more data to the stream_info dict
    if raindrop_path:
        stream_info["raindrop_pathDist"] = round(geod.geometry_length(raindrop_path), 2)

    # Split the flowline
    _, downstream_portion = split_flowline(intersection_point, nhd_flowline)

    # If the NHD Flowline was split, then calculate measure
    if downstream_portion:
        dist_to_outlet = round(geod.geometry_length(downstream_portion), 2)
        flowline_leng = round(geod.geometry_length(nhd_flowline), 2)
        stream_info["measure"] = round((dist_to_outlet / flowline_leng) * 100, 2)
    # If NHDFlowline was not split, then the intersection_point is either the
    # first or last point on the NHDFlowline
    else:
        start_pnt = Point(nhd_flowline.coords[0][0], nhd_flowline.coords[0][1])
        last_pnt_id = len(nhd_flowline.coords) - 1
        last_pnt = Point(
            nhd_flowline.coords[last_pnt_id][0],
            nhd_flowline.coords[last_pnt_id][1],
        )
        if intersection_point == start_pnt:
            stream_info["measure"] = 100
            error = "The point of intersection is the first point on the NHD Flowline."
        elif intersection_point == last_pnt:
            stream_info["measure"] = 0
            error = "The point of intersection is the last point on the NHD Flowline."
        elif intersection_point != start_pnt and intersection_point != last_pnt:
            error = "Error: NHD Flowline measure not calculated"
            stream_info["measure"] = "null"
        logger.warning(error)

    logger.info("calculated measure and reach")
    return stream_info


def split_flowline(
    intersection_point: Point,
    nhd_flowline: LineString,
) -> Tuple[Union[LineString, None], Union[LineString, None]]:
    """Split the NHD Flowline at the intersection point.

    Args:
        intersection_point (Point): The Shapely point at which to split the flowline
        nhd_flowline (LineString): The flowline to split

    Returns:
        A tuple containing two shapely LineString. The first is the upstream portion
        and the second is the donwstream portion of the input flowline. If the input
        linestring fails to be split, or the split point is the fist or last point
        on the line, then None values will be returned inplace of non-existance
        Shapely Linestrings.
    """
    # If the intersection_point is on the NHD Flowline, split the flowline at the point
    if nhd_flowline.intersects(intersection_point) is True:
        split_nhd_flowline = split(nhd_flowline, intersection_point)

    # If they don't intersect (weird right?), buffer the intersection_point
    # and then split the flowline
    if nhd_flowline.intersects(intersection_point) is False:
        logger.info("Intersection point does not intersect the NHD Flowline geometry (according to Shapely).")
        buff_ratio = 1.1
        buff_dist = intersection_point.distance(nhd_flowline) * buff_ratio
        buff_intersection_point = intersection_point.buffer(buff_dist)
        # Have had issues with the line not being split if the buff_dist is very small. This while
        # while attempts to split the line, and if it fails, then the buffer is increased.
        split_line = False
        while not split_line:
            try:
                split_nhd_flowline = split(nhd_flowline, buff_intersection_point)
                split_line = True
            except ValueError:
                buff_ratio += 1
                buff_intersection_point = intersection_point.buffer(buff_dist * buff_ratio)

    # If the NHD Flowline was split, then calculate measure
    if len(split_nhd_flowline.geoms) > 1:
        upstream_flowline = split_nhd_flowline.geoms[0]
        downstream_flowline = split_nhd_flowline.geoms[-1]

    else:  # If NHDFlowline was not split, then the intersection_point is either the
        # first or last point on the NHDFlowline
        start_pnt = Point(nhd_flowline.coords[0][0], nhd_flowline.coords[0][1])
        last_pnt_id = len(nhd_flowline.coords) - 1
        last_pnt = Point(
            nhd_flowline.coords[last_pnt_id][0],
            nhd_flowline.coords[last_pnt_id][1],
        )
        if intersection_point == start_pnt:
            upstream_flowline = None
            downstream_flowline = split_nhd_flowline
            error = "The point of intersection is the first point on the NHD Flowline."
        elif intersection_point == last_pnt:
            downstream_flowline = None
            upstream_flowline = split_nhd_flowline
            error = "The point of intersection is the last point on the NHD Flowline."
        elif intersection_point != start_pnt and intersection_point != last_pnt:
            error = "Error: NHD Flowline measure not calculated"
            downstream_flowline = None
            upstream_flowline = None
        logger.warning(error)

    logger.info("split NHD Flowline")
    return upstream_flowline, downstream_flowline
