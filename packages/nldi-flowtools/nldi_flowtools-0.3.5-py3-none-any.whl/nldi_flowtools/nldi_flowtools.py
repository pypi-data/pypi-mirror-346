"""Main module."""
import geojson

from nldi_flowtools.flowtrace import Flowtrace
from nldi_flowtools.splitcatchment import SplitCatchment


def splitcatchment(lon: float, lat: float, upstream: bool) -> geojson.FeatureCollection:
    """Delineate the drainage basin from the input point.

    This function identifies the local NHDP catchment containing the input 
    coordinates and determines the upstream drainage area. It returns the local 
    catchment and, depending on the `upstream` flag, either the split catchment 
    or the full upstream drainage basin.

    Parameters
    ----------
    lon : float
        Longitude coordinate of the input point in WGS 84 decimal degrees.
    lat : float
        Latitude coordinate of the input point in WGS 84 decimal degrees.
    upstream : bool
        - True: Returns the full upstream drainage basin.
        - False: Returns the portion of the drainage basin within the local catchment.

    Returns
    -------
    geojson.FeatureCollection 
        A GeoJSON FeatureCollection containing:

        - **Catchment (geojson.Feature)**: The NHD catchment. This is the catchment 
            that gets "split."
        - **SplitCatchment (geojson.Feature, optional)**: The portion of the catchment 
            upstream of the input point. This is included if `upstream=False`.
        - **DrainageBasin (geojson.Feature, optional)**: The full upstream drainage 
            basin if applicable. This is included if `upstream=True`.
    """
    return SplitCatchment(lon, lat, upstream).serialize()


def flowtrace(lon: float, lat: float, direction: str) -> geojson.FeatureCollection:
    """Trace the flowpath from a point to the nearest NHD flowline.

    Parameters
    ----------
    lon : float
        Longitude of the input point in WGS 84 decimal degrees.
    lat : float
        Latitude of the input point in WGS 84 decimal degrees.
    direction : str
        Specifies which portion of the NHD flowline to return:

        - "up": Returns the upstream portion of the intersected flowline.
        - "down": Returns the downstream portion of the intersected flowline.
        - "none": Returns the entire intersected flowline.

    Returns
    -------
    geojson.FeatureCollection
        A GeoJSON FeatureCollection containing:

        - **NHD Flowline (geojson.Feature)**: The intersected NHD stream segment, 
        which may be full, upstream, or downstream depending on `direction`.
        - **Raindrop Path (geojson.Feature)**: The traced path from the input 
        point to the NHD flowline.

    """
    return Flowtrace(lon, lat, direction).serialize()
