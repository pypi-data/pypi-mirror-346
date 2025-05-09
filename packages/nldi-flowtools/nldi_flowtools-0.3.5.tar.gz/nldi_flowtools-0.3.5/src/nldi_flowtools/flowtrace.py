"""Generate Raindrop Trace path using NLDI and user-defined point."""
from typing import Any
from typing import Tuple
from typing import Union

import geojson
from shapely.geometry import LineString
from shapely.geometry import Point

from nldi_flowtools.utils import check_coords
from nldi_flowtools.utils import get_coordsys
from nldi_flowtools.utils import get_facgrid
from nldi_flowtools.utils import get_flowgrid
from nldi_flowtools.utils import get_local_catchment
from nldi_flowtools.utils import get_local_flowline
from nldi_flowtools.utils import get_reach_measure
from nldi_flowtools.utils import JsonFeatureCollectionType
from nldi_flowtools.utils import project_point
from nldi_flowtools.utils import split_flowline
from nldi_flowtools.utils import trace_downhill
from nldi_flowtools.utils import transform_geom


class Flowtrace:
    """Trace downhill from a point to a stream.

    Given an longitude and latitude coordinate pair, the flow path will be trace
    downhill until it intersects a stream.
    This NHD stream can be cut at this point of intersection. With the
    third parameter, the user can specify whether they want the downstream or upstream
    portion of this stream, or its entire geometry. The flowpath from the query point
    to the stream will be returned as the second feature in the output.

    Args:
        x (float): Longitude coordinate
        y (float): Latitude coordinate
        direction (str): Portion of the NHD flowline to return
            - "down": Returns the downstream portion of the intersected stream.
            - "up": Returns the upstream portion of the intersected stream.
            - "none": Returns the full stream segment.

    Returns:
        raindropPath (geojson.Feature): The traced flow path from the query point 
            to the intersection point on the NHD flowline.
        nhdFlowline (geojson.Feature, optional): The full NHD stream segment intersected 
            by the flow trace. Only populated if `direction="none"`.
        upstreamFlowline (geojson.Feature, optional): The upstream portion of the 
            intersected NHD flowline. Only populated if `direction="up"`.
        downstreamFlowline (geojson.Feature, optional): The downstream portion of the 
            intersected NHD flowline. Only populated if `direction="down"`.
    """

    def __init__(self, x: float, y: float, direction: str) -> None:
        """Initialize Flowtrace."""
        self.x = x
        self.y = y
        self.direction = direction

        # outputs
        self.raindropPath: JsonFeatureCollectionType
        self.nhdFlowline: JsonFeatureCollectionType
        self.streamInfo: dict[str, Union[Tuple[Any, Any], str, float, None]]
        self.upstreamFlowline: JsonFeatureCollectionType
        self.downstreamFlowline: JsonFeatureCollectionType

        # kick off
        self.run()

    def serialize(self) -> geojson.FeatureCollection:  # noqa C901
        """Convert returns to GeoJSON to be exported.
        
        Returns a GeoJSON Feature Collection of the NHD stream segment
        and the raindropPath feature.
        """
        if self.direction == "up":
            nhd_feature = geojson.Feature(
                geometry=self.upstreamFlowline,
                id="upstreamFlowline",
                properties=self.streamInfo,
            )
            flowtrace_feature = geojson.Feature(geometry=self.raindropPath, id="raindropPath")

            return geojson.FeatureCollection([nhd_feature, flowtrace_feature])

        if self.direction == "down":
            nhd_feature = geojson.Feature(
                geometry=self.downstreamFlowline,
                id="downstreamFlowline",
                properties=self.streamInfo,
            )
            flowtrace_feature = geojson.Feature(geometry=self.raindropPath, id="raindropPath")

            return geojson.FeatureCollection([nhd_feature, flowtrace_feature])

        if self.direction == "none":
            nhd_feature = geojson.Feature(
                geometry=self.nhdFlowline,
                id="nhdFlowline",
                properties=self.streamInfo,
            )
            flowtrace_feature = geojson.Feature(geometry=self.raindropPath, id="raindropPath")

            return geojson.FeatureCollection([nhd_feature, flowtrace_feature])

    # main functions
    def run(self) -> None:  # noqa C901
        """Run Flowtrace module."""
        # Fetch the NHD catchment and flowline
        check_coords(self.x, self.y)
        transform_to_raster, transform_to_wgs84 = get_coordsys()
        catchment_id, catchment_geom = get_local_catchment(self.x, self.y)
        projected_catchment_geom = transform_geom(transform_to_raster, catchment_geom)
        flowline_json, flowline_geom = get_local_flowline(catchment_id)
        projected_flowline_geom = transform_geom(transform_to_raster, flowline_geom)
        projected_xy = project_point(self.x, self.y, transform_to_raster)

        # Open the flow direction and flow accumulation grids
        flw, fdr_profile = get_flowgrid(projected_catchment_geom)
        fac, fac_profile = get_facgrid(projected_catchment_geom)

        # Trace from the point to the NHD flowline (this will always run and return a flowpath)
        flowpath_coords, jumped_downstream = trace_downhill(
            projected_xy,
            fdr_profile["transform"],
            flw,
            fac,
            projected_flowline_geom,
            projected_catchment_geom,
            transform_to_wgs84,
            transform_to_raster,
        )

        # If the trace had to go to the downstream catchment, update the flowline data
        if jumped_downstream[0]:
            flowline_json, flowline_geom = jumped_downstream[1:]

        # The intersection point is the last point on the raindrop path, project back to WGS84
        raindrop_geom = transform_geom(transform_to_wgs84, LineString(flowpath_coords))
        raindrop_path = raindrop_geom.__geo_interface__
        intersection_point_geom = Point(raindrop_path["coordinates"][-1])

        # Outputs
        self.raindropPath = raindrop_path
        self.streamInfo = get_reach_measure(intersection_point_geom, flowline_json, raindrop_geom)
        if self.direction == "none":
            self.nhdFlowline = flowline_geom.__geo_interface__
        else:
            upstream_geom, downstream_geom = split_flowline(intersection_point_geom, flowline_geom)
            if self.direction == "up":
                self.upstreamFlowline = upstream_geom.__geo_interface__
            if self.direction == "down":
                self.downstreamFlowline = downstream_geom.__geo_interface__
