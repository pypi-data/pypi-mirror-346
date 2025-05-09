# NLDI Flowtools

NLDI Flowtools provides basin delineation and flow path tracing services.

[![PyPI](https://img.shields.io/pypi/v/nldi-flowtools.svg)](https://pypi.org/project/nldi-flowtools/)
[![Status](https://img.shields.io/pypi/status/nldi-flowtools.svg)](https://pypi.org/project/nldi-flowtools/)
[![Python Version](https://img.shields.io/pypi/pyversions/nldi-flowtools)](https://pypi.org/project/nldi-flowtools)
[![License](https://img.shields.io/pypi/l/nldi-flowtools)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)

[![Read the documentation at https://nldi-flowtools.readthedocs.io/](https://img.shields.io/readthedocs/nldi-flowtools/latest.svg?label=Read%20the%20Docs)](https://nldi-flowtools.readthedocs.io/)

[![pipeline status](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools/badges/main/pipeline.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools/-/commits/main)
[![coverage report](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools/badges/main/coverage.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools/-/commits/main)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Poetry](https://img.shields.io/badge/poetry-enabled-blue)](https://python-poetry.org/)
[![Conda](https://img.shields.io/badge/conda-enabled-green)](https://anaconda.org/)

# Description

NLDI Flowtools is a Python package which provides basin delineation and flow path tracing anywhere within CONUS from a WGS 84 latitude, longitude coordinate pair. This toolset uses NHDPlus Version 2 data to preform these tasks.

IPDS number: IP-143360

DOI number: doi:10.5066/P9W5UK7Z

# Documentation

Check out our documentation on Read the Docs: https://nldi-flowtools.readthedocs.io/en/latest/

# Requirements

Rasterio must be installed prior to installing NLDI-Flowtools. Package requirements are listed below.

- python = ">=3.10, <3.14"
- click = ">=7.1.2"
- geojson = "^2.5.0"
- numpy = ">=2.0.0"
- pyflwdir = "0.5.5"
- pyproj = "^3.4.0"
- rasterio = "^1.3.9"
- requests = "^2.32.0"
- Shapely = ">=2.0.0"

# Installation

## For users:

You can install _NLDI-Flowtools_ via
[pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/project/nldi-flowtools/):

```{.sourceCode .console}
$ pip install nldi-flowtools
```

## For Developers:

First, clone the repo. Navigate to the repo directory and create a new conda environment from the environment file.

```{.sourceCode .console}
$ conda env create -f environment.yaml
```

Then activate the environment and install the rest of the dependencies with Poetry.

```{.sourceCode .console}
$ conda activate nldi-flowtools
$ poetry install
```

Nox is used for organizing the suite of testing libraries used. To list all of the Nox test options, run:

```{.sourceCode .console}
$ nox --list
```

To run all of the Nox tests, simply run:

```{.sourceCode .console}
$ nox
```

To only run a single test, run:

```{.sourceCode .console}
$ nox -s mypy
```

# Features

- The Splitcatchment function delineates the drainage basin which is upstream from the input x,y point. Splitcatchment will return two polygons in geojson; the local National Hydrography Dataset (NHD) catchment which the input point falls in, and either the entire upstream drainage basin of that point or only the portion of the local catchment which drains to that point.
- The Flowtrace function traces the flowpath of water from the input point to the nearest NHD stream. Flowtrace returns two geojson linestrings; the first is the flow path which water will follow from the input point to the first down hill NHD stream, and the second linestring could be either the entire or the downstream or upstream segment of the NHD stream.

# Usage

In a python enviroment, first import nldi-flowtools, then either the Splitcatchment or Flowtrace function can be used. See [package documentation](https://nldi-flowtools.readthedocs.io/en/latest/) for additional details.

```{.sourceCode .console}
from nldi_flowtools.nldi_flowtools import splitcatchment, flowtrace

splitcatchment(-93, 45, True)
flowtrace(-93, 45, 'down')
```

The output:

```{.sourceCode .console}
{"features": [{"geometry": {"coordinates": [[[-93.004705, 44.992876], [-93.005282, 44.993016], [-93.005109, 44.994369], [-93.006721, 44.994937], [-93.009142, 44.995942], [-93.010043, 44.997435], [-93.01047, 44.998566], [-93.00983, 45.000034], [-93.012506, 45.002472], [-93.015846, 45.002357], [-93.016935, 45.00331], [-93.017277, 45.00575], [-93.018238, 45.006374], [-93.019473, 45.007456], [-93.016408, 45.009028], [-93.015893, 45.010429], [-93.014668, 45.010784], [-93.014747, 45.011952], [-93.017769, 45.011633], [-93.024573, 45.011535], [-93.027889, 45.012941], [-93.030205, 45.013294], [-93.030629, 45.014416], [-93.031776, 45.01516], [-93.032286, 45.015607], [-93.03194, 45.015903], [-93.031281, 45.016242], [-93.030671, 45.016766], [-93.028489, 45.017341], [-93.029079, 45.019437], [-93.025706, 45.019864], [-93.027294, 45.021279], [-93.027602, 45.021859], [-93.028008, 45.022373], [-93.028302, 45.023537], [-93.029097, 45.023471], [-93.030359, 45.024179], [-93.029554, 45.025062], [-93.030217, 45.026375], [-93.03126, 45.026981], [-93.030364, 45.029799], [-93.032025, 45.030167], [-93.032406, 45.030175], [-93.0322, 45.030856], [-93.031748, 45.031644], [-93.03232, 45.032858], [-93.029743, 45.033604], [-93.029815, 45.034658], [-93.027702, 45.036288], [-93.0263, 45.035378], [-93.025943, 45.033684], [-93.025622, 45.031789], [-93.024873, 45.032021], [-93.024379, 45.032741], [-93.022772, 45.033119], [-93.021788, 45.032783], [-93.021157, 45.03223], [-93.017605, 45.032519], [-93.016224, 45.033025], [-93.013402, 45.031829], [-93.01119, 45.031653], [-93.01077, 45.032538], [-93.010336, 45.033047], [-93.009851, 45.034901], [-93.007994, 45.035581], [-93.005658, 45.035661], [-93.004533, 45.035572], [-93.002982, 45.036141], [-93.001036, 45.036346], [-93.000267, 45.03716], [-92.998096, 45.038054], [-92.996288, 45.039504], [-92.996324, 45.040036], [-92.995239, 45.041315], [-92.994292, 45.044434], [-92.993428, 45.045099], [-92.992685, 45.045523], [-92.993941, 45.045954], [-92.995019, 45.046898], [-92.996678, 45.047975], [-92.995529, 45.048632], [-92.994894, 45.049558], [-92.993564, 45.050584], [-92.991463, 45.050305], [-92.990913, 45.050147], [-92.989704, 45.049861], [-92.988957, 45.048568], [-92.987572, 45.048094], [-92.988003, 45.047583], [-92.989156, 45.046925], [-92.989054, 45.045423], [-92.989749, 45.044602], [-92.989353, 45.039199], [-92.988922, 45.038918], [-92.989095, 45.038771], [-92.991664, 45.038093], [-92.99246, 45.036834], [-92.993813, 45.035626], [-92.993457, 45.034662], [-92.992063, 45.03385], [-92.991988, 45.033396], [-92.993936, 45.032882], [-92.995826, 45.031915], [-92.996018, 45.031162], [-92.995301, 45.030256], [-92.99576, 45.028457], [-92.995008, 45.027034], [-92.994565, 45.026475], [-92.993626, 45.024614], [-92.995175, 45.023822], [-92.994377, 45.023007], [-92.993673, 45.022114], [-92.992117, 45.022384], [-92.99068, 45.022746], [-92.989463, 45.022591], [-92.98908, 45.022622], [-92.988346, 45.022529], [-92.986211, 45.022898], [-92.984867, 45.024364], [-92.984216, 45.026253], [-92.982467, 45.025346], [-92.982309, 45.021084], [-92.981626, 45.019727], [-92.983246, 45.018395], [-92.983165, 45.017884], [-92.983407, 45.016933], [-92.982194, 45.015697], [-92.981423, 45.01423], [-92.980294, 45.013573], [-92.980431, 45.013026], [-92.979182, 45.012453], [-92.97737, 45.012222], [-92.976843, 45.013409], [-92.974682, 45.012643], [-92.975662, 45.010851], [-92.978939, 45.009987], [-92.979181, 45.009038], [-92.977167, 45.007864], [-92.976357, 45.006262], [-92.976527, 45.005596], [-92.976383, 45.004699], [-92.977253, 45.00395], [-92.978794, 45.00334], [-92.980416, 45.003547], [-92.981537, 45.003264], [-92.983643, 45.002999], [-92.984898, 45.001627], [-92.984371, 45.000631], [-92.983744, 45.000264], [-92.983425, 44.999952], [-92.984012, 44.999618], [-92.985005, 44.996917], [-92.98493, 44.995805], [-92.985013, 44.995279], [-92.986567, 44.993964], [-92.987134, 44.993134], [-92.98868, 44.993257], [-92.991361, 44.993165], [-92.993003, 44.993863], [-92.99399, 44.993828], [-92.99494, 44.993904], [-92.996622, 44.993846], [-92.997408, 44.993242], [-93.000138, 44.994857], [-93.001534, 44.994808], [-93.002847, 44.993796], [-93.003737, 44.993539], [-93.004283, 44.993116], [-93.004705, 44.992876]]], "type": "Polygon"}, "id": "catchment", "properties": {"catchmentID": "1100118"}, "type": "Feature"}, {"geometry": {"coordinates": [[[-93.002465, 45.000378], [-93.002477, 45.000109], [-93.002096, 45.000101], [-93.002108, 44.999831], [-92.999442, 44.999772], [-92.999454, 44.999502], [-92.999074, 44.999494], [-92.999086, 44.999224], [-92.998705, 44.999216], [-92.998717, 44.998946], [-92.998336, 44.998938], [-92.998288, 45.000015], [-92.998669, 45.000024], [-92.998657, 45.000293], [-93.002465, 45.000378]]], "type": "Polygon"}, "id": "splitCatchment", "properties": {}, "type": "Feature"}], "type": "FeatureCollection"}
{"features": [{"geometry": {"coordinates": [[-93.008717, 45.016322], [-93.009233, 45.016346], [-93.009942, 45.016507], [-93.010779, 45.016896], [-93.011134, 45.016942], [-93.01194, 45.016829], [-93.012714, 45.016578], [-93.013326, 45.016579], [-93.013745, 45.016716], [-93.01426, 45.017082], [-93.014292, 45.017243], [-93.01455, 45.017357], [-93.015807, 45.017427], [-93.016033, 45.017496], [-93.016644, 45.017885], [-93.01716, 45.018091], [-93.018159, 45.01839], [-93.019158, 45.018642], [-93.021253, 45.01853], [-93.021544, 45.018324], [-93.022028, 45.017776], [-93.022287, 45.01757], [-93.022673, 45.017571], [-93.023027, 45.017822], [-93.023221, 45.018051], [-93.023252, 45.01844], [-93.02325, 45.019606], [-93.023056, 45.020086], [-93.023054, 45.020909], [-93.023311, 45.021367], [-93.023665, 45.021733], [-93.02373, 45.021893], [-93.023761, 45.022487], [-93.023857, 45.022625], [-93.024373, 45.02274], [-93.025405, 45.022832], [-93.025823, 45.023038], [-93.025984, 45.023267], [-93.026015, 45.02425], [-93.026079, 45.024365], [-93.026046, 45.024479], [-93.026207, 45.024662], [-93.027624, 45.025692], [-93.02901, 45.026356], [-93.029815, 45.026654], [-93.030266, 45.026723], [-93.030782, 45.026678]], "type": "LineString"}, "id": "downstreamFlowline", "properties": {"comid": 1100118, "gnis_name": "none", "intersection_point": [45.016322, -93.008717], "measure": 71.31, "raindrop_pathDist": 2550.69, "reachcode": "07010206000564"}, "type": "Feature"}, {"geometry": {"coordinates": [[-93.000007, 44.999919], [-93.000388, 44.999928], [-93.000769, 44.999936], [-93.00115, 44.999945], [-93.001531, 44.999953], [-93.001911, 44.999962], [-93.00228, 45.000239], [-93.002661, 45.000248], [-93.003042, 45.000257], [-93.003423, 45.000265], [-93.003803, 45.000273], [-93.004184, 45.000282], [-93.004565, 45.00029], [-93.004553, 45.00056], [-93.004541, 45.000829], [-93.004529, 45.001099], [-93.004517, 45.001368], [-93.004505, 45.001638], [-93.004874, 45.001916], [-93.005255, 45.001924], [-93.005635, 45.001933], [-93.005623, 45.002202], [-93.005992, 45.00248], [-93.00598, 45.00275], [-93.006349, 45.003028], [-93.006337, 45.003297], [-93.006706, 45.003575], [-93.006694, 45.003844], [-93.006682, 45.004114], [-93.00667, 45.004383], [-93.006658, 45.004653], [-93.006646, 45.004922], [-93.006634, 45.005192], [-93.006241, 45.005453], [-93.005848, 45.005714], [-93.005836, 45.005983], [-93.005443, 45.006244], [-93.005431, 45.006514], [-93.0058, 45.006792], [-93.006169, 45.00707], [-93.006538, 45.007348], [-93.006526, 45.007617], [-93.006514, 45.007886], [-93.006502, 45.008156], [-93.00649, 45.008425], [-93.006478, 45.008695], [-93.006466, 45.008964], [-93.006835, 45.009242], [-93.006823, 45.009512], [-93.006811, 45.009781], [-93.006799, 45.010051], [-93.006787, 45.01032], [-93.006775, 45.01059], [-93.006763, 45.010859], [-93.006751, 45.011129], [-93.00712, 45.011406], [-93.007488, 45.011684], [-93.007476, 45.011954], [-93.007464, 45.012223], [-93.007452, 45.012493], [-93.007821, 45.012771], [-93.00819, 45.013049], [-93.008178, 45.013318], [-93.008166, 45.013588], [-93.008154, 45.013857], [-93.008535, 45.013866], [-93.008142, 45.014127], [-93.007749, 45.014388], [-93.007356, 45.014649], [-93.007344, 45.014918], [-93.007332, 45.015188], [-93.00732, 45.015457], [-93.007308, 45.015726], [-93.007296, 45.015996], [-93.007665, 45.016274], [-93.008046, 45.016282], [-93.008427, 45.016291], [-93.008717, 45.016322]], "type": "LineString"}, "id": "raindropPath", "properties": {}, "type": "Feature"}], "type": "FeatureCollection"}
```

# Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools/-/blob/master/CONTRIBUTING.md).

# License

Distributed under the terms of the [CC0 1.0 Universal license](https://creativecommons.org/publicdomain/zero/1.0/legalcode),
_NLDI Flowtools_ is free and open source software.

# Issues

If you encounter any problems,
please [file an issue](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools/-/issues) along with a detailed description.

# Disclaimer

[DISCLAIMER.md](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools/-/blob/master/DISCLAIMER.md)

# Authors

Anders Hopkins - _Lead Developer_ - [USGS Web Informatics & Mapping](https://wim.usgs.gov/)

# Citation

```{.sourceCode .console}
Hopkins, A.L., 2025, NLDI Flowtools, U.S. Geological Survey Software Release, https://doi.org/10.5066/P9W5UK7Z.
```

# Credits

- Streams and catchment geometries are queried from [NHDPlus Version 2](https://water.usgs.gov/catalog/datasets/8a60b6b4-d785-4265-af99-cd1870ea7928/) using the [Network Linked Data Index](https://waterdata.usgs.gov/blog/nldi-intro/).
- Flow direction and flow accumulation rasters from [NHDPlus Version 2 ](https://www.sciencebase.gov/catalog/item/66f42a51d34e791ae5dfc2ea) are also used in this package.
- This project was generated from
  [@hillc-usgs](https://github.com/hillc-usgs)'s [Pygeoapi Plugin
  Cookiecutter](https://code.usgs.gov/wma/nhgf/pygeoapi-plugin-cookiecutter)
  template.

## Acknowledgments

- This toolset was originally forked from [@marsmith](https://code.usgs.gov/marsmith)'s repo [ss-delineate](https://github.com/marsmith/ss-delineate).
- For the actual hydrologic delineations, we use the package [Pyfwldir](https://deltares.github.io/pyflwdir/latest/).
- This project was done in colaboration with [@rmcd](https://code.usgs.gov/rmcd)'s [NLDI XStools](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-xstool).
- The flow direction raster used for the delineations was put together as a cloud optimized geotiff and hosted it in AWS S3 by [@dblodgett](https://code.usgs.gov/dblodgett).
